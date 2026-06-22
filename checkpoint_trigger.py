import os
import csv
import folder_paths

# 【核心机制】启动时读取 TXT 并缓存
TRIGGER_MAP = {}
txt_path = os.path.join(os.path.dirname(__file__), "checkpoint_triggers.txt")

if os.path.exists(txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='=', quotechar='"')
            for row in reader:
                if len(row) >= 2:
                    lora_name = row[0].strip().lower()
                    triggers = row[1].strip()
                    TRIGGER_MAP[lora_name] = triggers
        print(f"[CheckpointTrigger] 成功从 TXT 加载 {len(TRIGGER_MAP)} 条参数映射。")
    except Exception as e:
        print(f"[CheckpointTrigger] 读取 TXT 失败: {e}")
else:
    print(f"[CheckpointTrigger] 未找到 checkpoint_triggers.txt")


class CheckpointLoaderWithTriggerDisplay:
    @classmethod
    def INPUT_TYPES(cls):
        # 获取所有 Checkpoint 列表
        checkpoint_list = folder_paths.get_filename_list("checkpoints")
        
        return {
            "required": {
                "ckpt_name": (checkpoint_list, ),
            },
            "optional": {
                "recommended_params": ("STRING", {
                    "multiline": True, 
                    "default": TRIGGER_MAP.get(checkpoint_list[0].lower() if checkpoint_list else "", "未找到推荐参数")
                }),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    FUNCTION = "load_checkpoint"
    CATEGORY = "loaders"

    def load_checkpoint(self, ckpt_name, recommended_params=""):
        # 执行标准的 Checkpoint 加载逻辑
        ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
        import comfy.utils
        out = comfy.sd.load_checkpoint_guess_config(
            ckpt_path, 
            output_vae=True, 
            output_clip=True, 
            embedding_directory=folder_paths.get_folder_paths("embeddings")
        )
        return out[:3]  # 返回 MODEL, CLIP, VAE

NODE_CLASS_MAPPINGS = {
    "CheckpointLoaderWithTriggerDisplay": CheckpointLoaderWithTriggerDisplay
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CheckpointLoaderWithTriggerDisplay": "Checkpoint Loader With Params"
}