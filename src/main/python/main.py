from lib.sound_and_text import SoundToSubTitle, read_cfg



class ExecutionKenrel(object):
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self):
        process_algo = SoundToSubTitle(cfg=self.cfg)
        process_algo.process()



if __name__ == "__main__":


    # === load parameter ===
    cfg_path = "C:/Users/murray/Desktop/realtime_japansese_translate/src/main/python/config/config.yml"
    cfg = read_cfg(cfg_path)
    
    # === read/translate/t2t/subtitle ===
    kernel = ExecutionKenrel(cfg=cfg)
    kernel.run()
    
