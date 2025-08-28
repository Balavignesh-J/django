from blog.models import Detail
from django.core.management.base import BaseCommand
import random


class Command(BaseCommand):
    help='auto import'
    
    def handle(self, *args, **options):
        Detail.objects.all().delete()
        titles = [
            "Django Tips", "Learning Python", "Web Development", "Data Science", "AI Future",
            "Coding Fun", "Tech Trends", "Open Source", "Programming Logic", "Backend Basics",
            "Frontend Hacks", "UI/UX Design", "Machine Learning", "Deep Learning", "Database Magic",
            "Cloud World", "APIs Everywhere", "Debugging Tricks", "Code Optimization", "System Design","Scalable Architectures",
            "Intro to Cybersecurity",
            "Data Visualization Secrets",
            "Testing Like a Pro",
            "DevOps Simplified",
            "Future of Quantum Computing",
            "Agile and Scrum Essentials",
            "Mobile App Development",
            "Handling Big Data"
        ]

        contents = [
            "This is a short blog content.",
            "Explaining some cool concepts here.",
            "A detailed walkthrough of an interesting topic.",
            "Quick tips for beginners and pros.",
            "Sharing thoughts about coding and development.",
            "Exploring the hidden gems of technology.",
            "Step by step guide for learners.",
            "Insights from real-world projects.",
            "Opinion on software trends.",
            "Best practices every developer should know.","Clean Code Matters",
             "Writing clean and maintainable code makes collaboration easier, reduces bugs, and ensures long-term project success.",
    "Designing scalable system architectures requires balancing performance, reliability, and future growth opportunities.",
    "Cybersecurity basics help developers safeguard applications from common vulnerabilities and potential attacks.",
    "Data visualization is not just charts; it’s about storytelling with numbers to reveal hidden insights effectively.",
    "Testing ensures software reliability. From unit testing to integration, proper testing saves time and cost.",
    "DevOps culture bridges the gap between development and operations, enabling faster delivery and continuous deployment.",
    "Quantum computing promises revolutionary advancements, but understanding the fundamentals is key to staying ahead.",
    "Agile and Scrum encourage iterative development, adaptability, and continuous feedback in modern project management.",
    "Mobile app development blends design, performance, and user experience into small yet powerful digital products.",
    "Big Data handling involves distributed systems, optimized queries, and tools like Hadoop and Spark for efficiency."
        ]

        img_urls = [
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300",
            "https://picsum.photos/200/300"
        ]

        for t,c,i in zip(titles,contents,img_urls):
            Detail.objects.create(title=t,content=c,img_url=i,category_id=random.randint(1,5))
        self.stdout.write(self.style.SUCCESS("completed"))