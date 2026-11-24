import os, urllib.request, torch, py_vncorenlp, gradio as gr
from transformers import AutoTokenizer, AutoModelForTokenClassification

SHARE = False   # True: Gradio tự cấp link công khai tạm. Dùng ngrok thì đổi thành False

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(ROOT, "Model", "model")
VN_DIR = r"C:\vncorenlp"

BASE = "https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/"
for f in ["VnCoreNLP-1.2.jar", "models/wordsegmenter/vi-vocab",
          "models/wordsegmenter/wordsegmenter.rdr"]:
    path = os.path.join(VN_DIR, *f.split("/"))
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(BASE + f, path)

seg = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=VN_DIR)
dev = "cuda" if torch.cuda.is_available() else "cpu"
tok = AutoTokenizer.from_pretrained(MODEL_DIR)
mdl = AutoModelForTokenClassification.from_pretrained(MODEL_DIR).to(dev).eval()


def tag(text):
    text = text[:500]
    res = []
    for sent in seg.word_segment(text):
        words, ids, first = sent.split(), [tok.cls_token_id], []
        for w in words:
            sub = tok.encode(w, add_special_tokens=False)
            if len(ids) + len(sub) >= 255:
                break
            first.append(len(ids))
            ids += sub
        ids.append(tok.sep_token_id)
        with torch.no_grad():
            p = mdl(input_ids=torch.tensor([ids], device=dev)).logits.argmax(-1)[0].tolist()
        for i, k in enumerate(first):
            res += [(words[i].replace("_", " "), mdl.config.id2label[p[k]]), (" ", None)]
    return res


demo = gr.Interface(
    fn=tag,
    inputs=gr.Textbox(lines=3, label="Nhập câu tiếng Việt"),
    outputs=gr.HighlightedText(label="Từ loại"),
    title="PhoBERT POS Tagging",
)
demo.queue(max_size=20)
demo.launch(server_name="127.0.0.1", server_port=7860, share=SHARE)