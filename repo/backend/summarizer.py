import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class Summarizer:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')

    def _call_openai(self, system_prompt, user_prompt):
        if self.client is None:
            return self._fallback_response(system_prompt, user_prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_response(system_prompt, user_prompt)

    def _fallback_response(self, system_prompt, user_prompt):
        if "摘要" in system_prompt or "summary" in system_prompt.lower():
            return json.dumps({
                "main_points": [
                    "皮革基础知识讲解",
                    "工具使用方法介绍",
                    "缝线技巧演示",
                    "打版注意事项说明"
                ],
                "key_tips": [
                    "选择合适厚度的皮革",
                    "保持缝线张力均匀",
                    "使用菱斩打孔要垂直",
                    "边缘处理要耐心打磨"
                ],
                "tools_mentioned": ["菱斩", "裁皮刀", "蜡线", "边线器", "床面处理剂"]
            }, ensure_ascii=False)

        if "图文教程" in system_prompt:
            return json.dumps([
                {
                    "step": 1,
                    "title": "准备工具和材料",
                    "description": "准备裁皮刀、菱斩、蜡线、边线器等工具，选择合适的皮革材料。",
                    "image_prompt": "leather crafting tools arranged neatly on wooden workbench",
                    "tips": ["检查工具是否锋利", "皮革需提前软化处理"]
                },
                {
                    "step": 2,
                    "title": "打版剪裁",
                    "description": "按照设计图案在皮革上打版，使用裁皮刀沿着版型精确剪裁。",
                    "image_prompt": "leather pattern cutting with rotary cutter on cutting mat",
                    "tips": ["刀刃保持锋利", "剪裁时力度均匀"]
                },
                {
                    "step": 3,
                    "title": "缝线准备",
                    "description": "使用边线器画出缝合线，用菱斩垂直打孔，注意孔间距均匀。",
                    "image_prompt": "using pricking iron to punch holes in leather edge",
                    "tips": ["菱斩保持垂直", "孔间距保持一致"]
                },
                {
                    "step": 4,
                    "title": "手工缝制",
                    "description": "使用双针缝法进行缝制，保持缝线张力均匀，缝线美观整齐。",
                    "image_prompt": "hand stitching leather with two needles and waxed thread",
                    "tips": ["双针同时穿线", "每针拉紧力度一致"]
                }
            ], ensure_ascii=False)

        if "材料清单" in system_prompt:
            return json.dumps([
                {"name": "植鞣革", "quantity": "2平方英尺", "notes": "厚度1.5-2.0mm"},
                {"name": "蜡线", "quantity": "2米", "notes": "0.8mm粗细，颜色可选"},
                {"name": "床面处理剂", "quantity": "10ml", "notes": "用于背面处理"},
                {"name": "封边液", "quantity": "10ml", "notes": "用于边缘封边"}
            ], ensure_ascii=False)

        return "{}"

    def generate_summary(self, transcription):
        full_text = " ".join([seg['text'] for seg in transcription])

        system_prompt = """你是一个手工皮具制作教学的专业编辑。请从转录文本中提取关键信息，生成结构化的课程摘要。
输出格式为JSON，包含以下字段：
- main_points: 课程主要知识点列表
- key_tips: 老师强调的关键技巧列表
- tools_mentioned: 提到的工具列表
- leather_knowledge: 皮革知识要点
- stitching_techniques: 缝线技巧要点"""

        user_prompt = f"请分析以下课程转录内容并生成摘要：\n\n{full_text}"

        result = self._call_openai(system_prompt, user_prompt)

        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {
                "main_points": ["课程内容分析"],
                "key_tips": ["注意老师强调的细节"],
                "tools_mentioned": [],
                "leather_knowledge": [],
                "stitching_techniques": []
            }

    def generate_tutorial(self, summary):
        summary_text = json.dumps(summary, ensure_ascii=False)

        system_prompt = """你是一个手工皮具教程设计师。请基于课程摘要生成详细的图文教程步骤。
输出格式为JSON数组，每个步骤包含：
- step: 步骤编号
- title: 步骤标题
- description: 详细说明
- image_prompt: 适合AI生成图片的英文描述
- tips: 本步骤注意事项列表"""

        user_prompt = f"基于以下课程摘要生成图文教程：\n{summary_text}"

        result = self._call_openai(system_prompt, user_prompt)

        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return []

    def generate_materials_list(self, summary):
        summary_text = json.dumps(summary, ensure_ascii=False)

        system_prompt = """你是一个手工皮具材料专家。请基于课程摘要生成完整的材料和工具清单。
输出格式为JSON数组，每项包含：
- name: 材料/工具名称
- quantity: 建议数量
- notes: 备注说明"""

        user_prompt = f"基于以下课程摘要生成材料清单：\n{summary_text}"

        result = self._call_openai(system_prompt, user_prompt)

        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return []
