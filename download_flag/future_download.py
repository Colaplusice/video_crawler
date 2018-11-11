from concurrent import futures
from base_download import save_flag, get_flag, main, show
from download_flag.configs import MAX_WORKERS, CC_LIST
from utils import timer


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, '{}.gif'.format(cc))
    return cc



@timer
def download_many(cc_list):
    worker_num = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(worker_num) as executor:
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


@timer
def download_many_2(cc_list):
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        msg = 'Scheduled for {} {}'

        for cc in cc_list:
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print(msg.format(cc, future))

        results = []
        msg = '{} result : {!r}'

        for future in futures.as_completed(to_do):
            res = future.result()
            print(msg.format(future, res))
            results.append(res)
    return len(results)


if __name__ == '__main__':
    # download_many(cc_list=CC_LIST)
    download_many_2(cc_list=CC_LIST)
