from os import path, remove, makedirs, stat
from typing import List, Mapping
from dataclasses import dataclass, asdict
from requests import Session
from logging import getLogger
from json import dump, load
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
logger = getLogger('sssekai.abcache')

from sssekai.crypto.APIManager import decrypt
from sssekai.crypto.AssetBundle import decrypt_headaer_inplace, SEKAI_AB_MAGIC
from msgpack import unpackb
from tqdm import tqdm
DEFAULT_CACHE_DIR = '~/.sssekai/abcache'
# 2.6.1
SEKAI_CDN = 'https://production-cf2d2388-assetbundle-info.sekai.colorfulpalette.org/'
SEKAI_AB_CDN = 'https://production-cf2d2388-assetbundle.sekai.colorfulpalette.org/'
SEKAI_AB_BASE_PATH = '3.3.0.20/8fd5e993-0146-c881-8902-4ed113efcdbf/android/'
SEKAI_AB_INDEX_PATH = 'api/version/3.3.0.20/os/android'
# HACK: Bypasses the check for now. Would this expire though?
SEKAI_API_COOKIES = 'CloudFront-Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcwNzcwNDc1Nn0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIwLjAuMC4wLzAifX19XX0_; CloudFront-Signature=KKEPARo-8R5aSq~AsEyXL~Bl7OaZ5P7U7KhxcQCjCtgVeCTdLxehu3fUt22cS-UOg25ZhzLLc4vEsFFTAz4LPq~I7lOZcGNj5Jan5-fQg52iRHVnZw~otkRrrsyZh6aDnKMxeNmqSOBtvf4Nw0tqe6vRPo398l6IqBeHZ-5owKQxG0SreAmq1wm8VSnMTow2l5Atxw~reEqQ9TFsktMsebL1eqExROXF4e~135zrcFuN9C~vPOs4m9CogLaYKPXcCau-l1D~Qs7PXXL3ZSY6r40kwdICfd50MiVM14Ip~926Xh6MO3BfEGR20WFqCA-VPGfa3ANUHR9Rj-Gzddxlrw__; CloudFront-Key-Pair-Id=KV6QGCE0D633X;'
class ThreadpoolDownloader(ThreadPoolExecutor):
    session : Session
    progress : tqdm

    def download(self, url, fname, length):
        RETRIES = 1
        for _ in range(0,RETRIES):
            try:
                resp = self.session.get(url,stream=True)
                resp.raise_for_status()
                makedirs(path.dirname(fname),exist_ok=True)
                with open(fname, 'wb') as f:
                    magic = next(resp.iter_content(4))
                    if magic == SEKAI_AB_MAGIC:
                        header = next(resp.iter_content(128))            
                        self.progress.update(128)
                        f.write(decrypt_headaer_inplace(bytearray(header)))
                    else:
                        f.write(magic)                
                    for chunk in resp.iter_content(65536):
                        self.progress.update(len(chunk))
                        f.write(chunk)
                    return
            except Exception as e:
                logger.error('While downloading %s : %s. Retrying' % (url,e))
        if _ == RETRIES - 1:
            logger.critical('Did not download %s' % url)
    def add_link(self, url, fname, length):
        self.progress.total += length
        return self.submit(self.download, url, fname, length)
    def __init__(self, session = None) -> None:
        self.session = session or Session()
        self.progress = tqdm(bar_format="{desc}: {percentage:.1f}%|{bar}| {n_fmt}/{total_fmt} {rate_fmt} {elapsed}<{remaining}", total=0,unit='B', unit_scale=True, unit_divisor=1024,desc="Downloading")
        super().__init__() # workers = processor count * 5

class AbCacheConfig:
    cache_dir : str # absolute path to cache directory
    downloader : ThreadpoolDownloader
    def __init__(self, downloader : ThreadpoolDownloader, cache_dir: str = DEFAULT_CACHE_DIR) -> None:
        self.cache_dir = path.expanduser(cache_dir)
        self.cache_dir = path.abspath(self.cache_dir)
        self.downloader = downloader

@dataclass
class AbCacheEntry(dict):
    bundleName: str
    cacheFileName: str
    cacheDirectoryName: str
    hash: str
    category: str
    crc: int
    fileSize:int
    dependencies : List[str]
    paths : List[str]
    isBuiltin : bool

    def up_to_date(self, config: AbCacheConfig, other) -> bool:
        fsize = self.get_file_size(config)     
        return self.hash == other.hash and self.fileSize <= fsize # fsize may be fileSize + 4
    
    def get_file_size(self, config: AbCacheConfig):
        if self.get_file_exists(config):
            return stat(self.get_file_path(config)).st_size
        else:
            return 0

    def get_file_exists(self, config: AbCacheConfig) -> bool:
        return path.exists(self.get_file_path(config))
    
    def get_file_path(self, config: AbCacheConfig) -> str:
        return path.join(config.cache_dir, self.bundleName)
@dataclass
class AbCacheIndex(dict):
    version : str = 'unknown'
    os : str = 'android'
    bundles : Mapping[str, AbCacheEntry] = None
    def get_bundle_by_abcache_path(self, config: AbCacheConfig, fpath) -> AbCacheEntry | None:
        # "C:\Users\mos9527\.sssekai\abcache\title_screen\anniversary_2nd_bg"
        fpath = Path(fpath)
        cpath = Path(config.cache_dir)
        assert fpath.is_relative_to(cpath), "File provided is not inside the cache"
        relpath = fpath.relative_to(cpath).as_posix()
        return self.bundles.get(relpath,None)
    
class AbCache(Session):
    config : AbCacheConfig
    index : AbCacheIndex
    
    def download_cache_index(self) -> AbCacheIndex:
        resp = self.get(
            url=SEKAI_CDN + SEKAI_AB_INDEX_PATH,
            headers={
                'Accept-Encoding': 'deflate, gzip'
            }
        )
        resp.raise_for_status()
        data = decrypt(resp.content)
        data = unpackb(data)
        cache = AbCacheIndex(**data)
        for k,v in cache.bundles.items():
            cache.bundles[k] = AbCacheEntry(**v)
        return cache

    def update_cahce_entry(self, entry : AbCacheEntry, new_entry : AbCacheEntry = None):
        if new_entry:
            entry = new_entry
        return self.config.downloader.add_link(
            SEKAI_AB_CDN + SEKAI_AB_BASE_PATH + entry.bundleName,
            entry.get_file_path(self.config),
            entry.fileSize
        )
                
    def update_cahce_index(self):
        logger.info('Downloading Asset Bundle Index')
        dl = self.download_cache_index()
        all_keys = sorted(list({k for k in dl.bundles.keys()}.union({k for k in self.index.bundles.keys()})))
        update_count = 0
        for k in all_keys:
            if k in dl.bundles and k in self.index.bundles:
                # update
                if not dl.bundles[k].up_to_date(self.config, self.index.bundles[k]):
                    logger.info('Updating bundle %s', k)
                    self.update_cahce_entry(self.index.bundles[k], dl.bundles[k])
                    update_count+=1
                else:
                    logger.debug('Bundle %s is up to date' % k)
                    pass
            elif k in dl.bundles: 
                # append
                logger.debug('Adding bundle %s', k)
                self.index.bundles[k] = dl.bundles[k]
                self.update_cahce_entry(self.index.bundles[k])
                update_count+=1
            else: 
                # removal
                logger.info('Removing bundle %s', k)
                if path.exists(self.index.bundles[k].get_file_path(self.config)):
                    remove(self.index.bundles[k].get_file_path(self.config))
                del self.index.bundles[k]
        logger.info('Saving AssetBundle index')
        self.save()
        logger.info('...Saved. Need %d updates' % update_count)
        self.config.downloader.shutdown(wait=True)
        logger.info('AssetBundles are now up-to-date')
    
    def __init__(self, config : AbCacheConfig) -> None:
        super().__init__()        
        self.headers['Cookie'] = SEKAI_API_COOKIES
        self.config = config
        makedirs(self.config.cache_dir,exist_ok=True)
        try:
            self.load()
        except Exception as e:
            logger.warning('Failed to load cache index. Creating new one. (%s)' % e)
            self.index = AbCacheIndex(bundles=dict())
            self.save()
    
    def save(self):
        with open(path.join(self.config.cache_dir, 'abindex.json'),'w',encoding='utf-8') as f:
            dump(asdict(self.index), f, indent=4, ensure_ascii=False)
            logger.info("Saved %d entries to cache index" % len(self.index.bundles))

    def load(self):
        with open(path.join(self.config.cache_dir, 'abindex.json'),'r',encoding='utf-8') as f:
            self.index = AbCacheIndex(**load(f))
            for k,v in self.index.bundles.items():
                self.index.bundles[k] = AbCacheEntry(**v)
            logger.info("Loaded %d entries from cache index" % len(self.index.bundles))