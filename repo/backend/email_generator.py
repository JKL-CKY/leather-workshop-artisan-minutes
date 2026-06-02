import json
from datetime import datetime


class EmailGenerator:
    def generate_markdown_email(self, teacher_name, transcription, summary, tutorial, materials):
        timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M")

        md_content = []
        md_content.append(f"# 匠人纪要 · 手工皮具工坊课程笔记")
        md_content.append("")
        md_content.append(f"**授课老师：** {teacher_name}")
        md_content.append(f"**生成时间：** {timestamp}")
        md_content.append("")
        md_content.append("---")
        md_content.append("")

        md_content.append("## 📝 课程摘要")
        md_content.append("")
        if isinstance(summary, dict):
            if 'main_points' in summary and summary['main_points']:
                md_content.append("### 主要知识点")
                for point in summary['main_points']:
                    md_content.append(f"- {point}")
                md_content.append("")

            if 'key_tips' in summary and summary['key_tips']:
                md_content.append("### 关键技巧")
                for tip in summary['key_tips']:
                    md_content.append(f"- {tip}")
                md_content.append("")

            if 'leather_knowledge' in summary and summary['leather_knowledge']:
                md_content.append("### 皮革知识")
                for knowledge in summary['leather_knowledge']:
                    md_content.append(f"- {knowledge}")
                md_content.append("")

            if 'stitching_techniques' in summary and summary['stitching_techniques']:
                md_content.append("### 缝线技巧")
                for technique in summary['stitching_techniques']:
                    md_content.append(f"- {technique}")
                md_content.append("")

            if 'tools_mentioned' in summary and summary['tools_mentioned']:
                md_content.append("### 涉及工具")
                md_content.append(", ".join(summary['tools_mentioned']))
                md_content.append("")

        md_content.append("---")
        md_content.append("")

        md_content.append("## 🛠️ 图文教程")
        md_content.append("")
        if isinstance(tutorial, list):
            for step in tutorial:
                md_content.append(f"### 步骤 {step.get('step', '')}：{step.get('title', '')}")
                md_content.append("")
                md_content.append(f"{step.get('description', '')}")
                md_content.append("")
                if 'image_prompt' in step:
                    md_content.append(f"![{step.get('title', '')}](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={step['image_prompt']}&image_size=landscape_16_9)")
                    md_content.append("")
                if 'tips' in step and step['tips']:
                    md_content.append("**注意事项：**")
                    for tip in step['tips']:
                        md_content.append(f"- {tip}")
                md_content.append("")

        md_content.append("---")
        md_content.append("")

        md_content.append("## 📦 材料清单")
        md_content.append("")
        md_content.append("| 材料/工具 | 数量 | 备注 |")
        md_content.append("|----------|------|------|")
        if isinstance(materials, list):
            for item in materials:
                md_content.append(f"| {item.get('name', '')} | {item.get('quantity', '')} | {item.get('notes', '')} |")
        md_content.append("")

        md_content.append("---")
        md_content.append("")

        md_content.append("## 📹 完整转录")
        md_content.append("")
        md_content.append("<details>")
        md_content.append("<summary>点击展开完整转录内容</summary>")
        md_content.append("")
        for seg in transcription:
            start_time = self._format_time(seg.get('start', 0))
            end_time = self._format_time(seg.get('end', 0))
            speaker = seg.get('speaker', '老师')
            text = seg.get('text', '')
            md_content.append(f"`[{start_time} - {end_time}]` **{speaker}**：{text}")
            md_content.append("")
        md_content.append("</details>")
        md_content.append("")

        md_content.append("---")
        md_content.append("")
        md_content.append("*本笔记由匠人纪要系统自动生成*")

        return "\n".join(md_content)

    def _format_time(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
