import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Comfy.CheckpointTriggerStaticCopy",

    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "CheckpointLoaderWithTriggerDisplay") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                const paramWidget = this.widgets.find((w) => w.name === "recommended_params");
                const ckptWidget = this.widgets.find((w) => w.name === "ckpt_name");

                if (paramWidget) {
                    paramWidget.inputEl.readOnly = true;
                    paramWidget.inputEl.style.opacity = 0.8;
                }

                // 添加复制按钮
                const copyBtn = document.createElement("button");
                copyBtn.textContent = "Copy Params";
                copyBtn.style.marginTop = "2px";
                copyBtn.style.cursor = "pointer";
                copyBtn.onclick = () => {
                    if (paramWidget) {
                        navigator.clipboard.writeText(paramWidget.value).then(() => {
                            const originalText = copyBtn.textContent;
                            copyBtn.textContent = "Copied!";
                            setTimeout(() => copyBtn.textContent = originalText, 1000);
                        });
                    }
                };
                paramWidget.element.appendChild(copyBtn);

                // 核心联动：监听 Checkpoint 下拉框变化
                if (ckptWidget && paramWidget) {
                    const originalCallback = ckptWidget.callback;
                    ckptWidget.callback = async (value) => {
                        if (originalCallback) originalCallback(value);
                        
                        // 获取映射表
                        if (!window.CHECKPOINT_TRIGGER_MAP) {
                            try {
                                const resp = await fetch("/checkpoint_trigger_map");
                                window.CHECKPOINT_TRIGGER_MAP = await resp.json();
                            } catch(e) {
                                console.error("获取参数映射失败", e);
                            }
                        }

                        const lowerValue = value.toLowerCase();
                        if (window.CHECKPOINT_TRIGGER_MAP && window.CHECKPOINT_TRIGGER_MAP[lowerValue]) {
                            let rawParams = window.CHECKPOINT_TRIGGER_MAP[lowerValue];
                            paramWidget.value = rawParams.replace(/\\n/g, '\n');
                            paramWidget.inputEl.value = paramWidget.value;
                        } else {
                            paramWidget.value = "未找到推荐参数";
                        }
                    };
                    
                    // 页面加载时自动执行一次
                    ckptWidget.callback(ckptWidget.value);
                }

                return r;
            };
        }
    }
});