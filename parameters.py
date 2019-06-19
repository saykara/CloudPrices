class CloudParameters:
    region = ["Japan", "UK", "US East", "US West"] #, "Asia Pacific", "US Central"]
    os = ["Windows", "Ubuntu"]
    brand = ["Google", "Azure", "Amazon"] #, "Ali Baba"
    s_type = ["SSD", "HDD"]
    s_capacity = [128, 256, 512, 1024, 2048, 4096]
    cpu = [1, 2, 4]
    ram = [2, 4, 8, 16]
    ram = {'1': [2],
           '2': [4, 14],
           '4': [8, 28]}

    p_cpu = 64
    p_ram = 128
    p_ssd = 10240
    p_hdd = 20480


class DatabaseParameters:
    region_dict = (
        {"region": "Japan"},
        {"region": "UK"},
        {"region": "US East"},
        {"region": "US West"})

    brand_dict = ({"brand": "Amazon"},
                  {"brand": "Azure"},
                  {"brand": "Google"})
