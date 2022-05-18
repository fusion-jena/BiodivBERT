from subprocess import Popen, PIPE
from xml.etree.ElementTree import fromstring
from util_log import log

def get_gpu_info(*args, **kwargs):
    p = Popen(["nvidia-smi", "-q", "-x"], stdout=PIPE)
    outs, errors = p.communicate()
    xml = fromstring(outs)
    datas = []
    driver_version = xml.findall("driver_version")[0].text
    cuda_version = xml.findall("cuda_version")[0].text

    for gpu_id, gpu in enumerate(xml.getiterator("gpu")):
        gpu_data = {}
        name = [x for x in gpu.getiterator("product_name")][0].text
        memory_usage = gpu.findall("fb_memory_usage")[0]
        total_memory = memory_usage.findall("total")[0].text

        log.info('gpu_name: {}'.format(name))
        gpu_data["name"] = name

        gpu_data["total_memory"] = total_memory
        log.info('total_memory: {}'.format(total_memory))

        gpu_data["driver_version"] = driver_version
        log.info('driver_version: {}'.format(driver_version))

        gpu_data["cuda_version"] = cuda_version
        log.info('cuda_version: {}'.format(cuda_version))

        datas.append(gpu_data)

    return datas

if __name__ == '__main__':
    log.info('starting')
    get_gpu_info()