from concurrent.futures import ThreadPoolExecutor, Future

from .option import *


class ExhantaiDownloader:
    def __init__(self,
                 option: ExhentaiOption,
                 client: ExhentaiClient,
                 ):
        self.option = option
        self.client = client
        self.page_workers = ThreadPoolExecutor(max_workers=self.option.decide_download_page_workers())
        self.image_workers = ThreadPoolExecutor(max_workers=self.option.decide_download_image_workers())

    def download_gallery(self, gid: str, token: str, ):
        pic_url_dict: dict[str, str] = {}
        # fetch all pic_url (https://exhentai.org/s/xx/xx) of gallery

        # first page
        book = self.client.fetch_gallery_page(gid, token, p=0)
        pic_url_dict.update(book.pageInfo.picUrl)

        # the rest page
        # for p in range(1, book.page_count):
        #     book = self.client.fetch_gallery_page(gid, token, p)
        #     pic_url_dict.update(book.pic_url_dict)

        image_futures: list[Future] = []

        def run(p):
            pic_url = self.client.fetch_gallery_page(gid, token, p).pageInfo.picUrl
            pic_url_dict.update(pic_url)

            for index, pic_url in pic_url_dict.items():
                f = self.image_workers.submit(self.download_pic, index, pic_url, book)
                image_futures.append(f)

        self.run_all(
            iterables=range(1, book.page_count),
            apply=run,
            wait=True,
        )

        for f in image_futures:
            f.result()

    def download_pic(self, index: str, pic_url: str, book: BookInfo):
        resp = self.client.fetch_pic_page(pic_url)
        hurl, furl = ExhentaiHtmlParser.parse_hash_full_img_url(resp.text, pic_url)
        durl, path = self.option.decide_img_download_plan(book, int(index), hurl, furl, self.client)
        if durl is None:
            return

        self.download_image(durl, path)

    def download_image(self, img_url: str, path: str):
        self.client.download_image(img_url, path)

    def run_all(self, iterables, apply, wait=True):
        future_list = []

        for obj in iterables:
            args, kwargs = common.process_single_arg_to_args_and_kwargs(obj)
            f = self.page_workers.submit(apply, *args, **kwargs)
            future_list.append(f)

        if wait is True:
            for f in future_list:
                f.result()
