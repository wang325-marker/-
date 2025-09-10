from DrissionPage import WebPage
from DrissionPage.common import By
import csv
import time
import re
from urllib.parse import urljoin
import os


class Spider():
    def __init__(self):
        self.url = "https://mitadmissions.org/blogs/"
        self.browser = WebPage()
        self.data = []
        
    def get_blog_list(self):
        """获取博客列表页面的所有文章链接"""
        print("正在访问博客列表页面...")
        self.browser.get(self.url)
        time.sleep(3)  # 等待页面加载
        
        # 根据HTML结构，查找所有博客文章项
        blog_items = self.browser.eles('.tease-feed-item')
        print(f"找到 {len(blog_items)} 篇文章")
        
        blog_links = []
        for item in blog_items:
            try:
                # 获取文章链接
                link_element = item.ele('.post-tease__h__link', timeout=2)
                if link_element:
                    href = link_element.attr('href')
                    if href:
                        full_url = urljoin(self.url, href)
                        blog_links.append(full_url)
                        print(f"找到文章链接: {full_url}")
            except Exception as e:
                print(f"获取文章链接时出错: {e}")
                continue
                
        return blog_links
    
    def get_article_details(self, article_url):
        """获取单篇文章的详细信息"""
        print(f"正在抓取文章: {article_url}")
        
        try:
            self.browser.get(article_url)
            time.sleep(2)  # 等待页面加载
            
            # 初始化数据字典
            article_data = {
                'title': '',
                'author': '',
                'comments': '0',
                'time': '',
                'content': '',
                'images': ''
            }
            
            # 获取标题
            try:
                title_element = self.browser.ele('.page-topper__title', timeout=3)
                if title_element:
                    article_data['title'] = title_element.text.strip()
                else:
                    # 尝试其他可能的标题选择器
                    title_element = self.browser.ele('h1', timeout=2)
                    if title_element:
                        article_data['title'] = title_element.text.strip()
            except:
                article_data['title'] = '未找到标题'
            
            # 获取作者
            try:
                author_element = self.browser.ele('.page-topper__title__name', timeout=3)
                if author_element:
                    article_data['author'] = author_element.text.strip()
                else:
                    # 尝试其他可能的作者选择器
                    author_element = self.browser.ele('.article__author-h', timeout=2)
                    if author_element:
                        article_data['author'] = author_element.text.strip()
            except:
                article_data['author'] = '未知作者'
            
            # 获取时间
            try:
                time_element = self.browser.ele('.page-topper__date', timeout=3)
                if time_element:
                    article_data['time'] = time_element.text.strip()
                else:
                    # 尝试其他可能的时间选择器
                    time_element = self.browser.ele('[datetime]', timeout=2)
                    if time_element:
                        article_data['time'] = time_element.attr('datetime') or time_element.text.strip()
            except:
                article_data['time'] = '未知时间'
            
            # 获取文章内容 - 修改版本
            try:
                # 方法1：尝试获取包含文章内容的div容器
                content_container = self.browser.ele('.article__body.js-hang-punc', timeout=3)
                if content_container:
                    # 获取div内所有的p标签
                    content_elements = content_container.eles('p')
                    if content_elements:
                        content_texts = []
                        for elem in content_elements:
                            # 获取p标签的完整文本内容（包括span标签内的文本）
                            text = elem.text.strip()
                            if text and len(text) > 10:  # 过滤掉太短的段落
                                content_texts.append(text)
                        
                        # 将所有段落拼接成完整文章，不限制长度
                        if content_texts:
                            article_data['content'] = '\n\n'.join(content_texts)
                        else:
                            article_data['content'] = content_container.text.strip()
                    else:
                        # 如果没找到p标签，尝试获取整个div的文本
                        article_data['content'] = content_container.text.strip()
                else:
                    # 备用方案：直接查找所有p标签
                    all_p_elements = self.browser.eles('p', timeout=3)
                    if all_p_elements:
                        content_texts = []
                        for elem in all_p_elements:
                            text = elem.text.strip()
                            # 过滤掉可能的导航或其他非内容p标签
                            if text and len(text) > 10:  # 只保留长度大于10的段落
                                content_texts.append(text)
                        article_data['content'] = '\n\n'.join(content_texts)
                    else:
                        article_data['content'] = '未找到内容'
                        
            except Exception as e:
                print(f"获取文章内容时出错: {e}")
                article_data['content'] = '内容获取失败'
            
            # 获取图片链接
            try:
                # 获取所有wp-caption aligncenter的div容器
                wp_caption_divs = self.browser.eles('.wp-caption.aligncenter', timeout=3)
                img_urls = []

                if wp_caption_divs:
                    # 遍历每个wp-caption div
                    for div in wp_caption_divs:
                        # 获取该div内的所有img标签
                        images = div.eles('img')
                        for img in images:
                            src = img.attr('src')
                            if src:
                                full_img_url = urljoin(article_url, src)
                                img_urls.append(full_img_url)

                    # 如果找到了图片，保存链接
                    if img_urls:
                        article_data['images'] = '; '.join(img_urls[:5])  # 限制最多5张图片
                    else:
                        # 如果wp-caption div中没有图片，尝试其他方式
                        all_images = self.browser.eles('img', timeout=2)
                        if all_images:
                            for img in all_images[:5]:
                                src = img.attr('src')
                                if src:
                                    full_img_url = urljoin(article_url, src)
                                    img_urls.append(full_img_url)
                            article_data['images'] = '; '.join(img_urls)
                        else:
                            article_data['images'] = '无图片'
                else:
                    # 如果没有找到wp-caption div，尝试获取页面顶部的特色图片
                    feature_img = self.browser.ele('.page-topper__img img', timeout=2)
                    if feature_img:
                        src = feature_img.attr('src')
                        if src:
                            article_data['images'] = urljoin(article_url, src)
                    else:
                        # 最后的备用方案：获取任意图片
                        all_images = self.browser.eles('img', timeout=2)
                        if all_images:
                            img_urls = []
                            for img in all_images[:3]:  # 最多3张图片作为备用
                                src = img.attr('src')
                                if src:
                                    full_img_url = urljoin(article_url, src)
                                    img_urls.append(full_img_url)
                            article_data['images'] = '; '.join(img_urls)
                        else:
                            article_data['images'] = '无图片'
                            
            except Exception as e:
                print(f"获取图片时出错: {e}")
                article_data['images'] = '无图片'
            
            # 获取评论数（MIT博客可能没有评论功能，设为0）
            article_data['comments'] = '0'
            
            print(f"成功抓取文章: {article_data['title']}")
            return article_data
            
        except Exception as e:
            print(f"抓取文章详情时出错: {e}")
            return None

    def save_to_csv(self, filename='mit_blogs.csv'):
        """将数据保存到CSV文件"""
        if not self.data:
            print("没有数据可保存")
            return
            
        print(f"正在保存数据到 {filename}...")
        
        # 确保题3目录存在
        os.makedirs('题3', exist_ok=True)
        filepath = os.path.join('题3', filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['标题', '作者', '评论数', '时间', '文章内容', '文章图片']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # 写入表头
            writer.writeheader()
            
            # 写入数据
            for item in self.data:
                writer.writerow({
                    '标题': item['title'],
                    '作者': item['author'],
                    '评论数': item['comments'],
                    '时间': item['time'],
                    '文章内容': item['content'],
                    '文章图片': item['images']
                })
        
        print(f"数据已保存到 {filepath}，共 {len(self.data)} 条记录")
    
    def main(self):
        """主函数"""
        try:
            print("开始抓取MIT招生博客...")
            
            # 获取博客列表
            blog_links = self.get_blog_list()
            
            if not blog_links:
                print("未找到任何博客文章链接")
                return
            
            print(f"准备抓取 {len(blog_links)} 篇文章的详细信息...")
            
            # 抓取每篇文章的详细信息
            for i, link in enumerate(blog_links[:10], 1):  # 限制抓取前10篇文章
                print(f"正在处理第 {i}/{min(len(blog_links), 10)} 篇文章...")
                
                article_data = self.get_article_details(link)
                if article_data:
                    self.data.append(article_data)
                
                # 添加延时避免请求过快
                time.sleep(2)
            
            # 保存数据到CSV
            self.save_to_csv()
            
            print("抓取完成！")
            
        except Exception as e:
            print(f"程序执行出错: {e}")
        finally:
            # 关闭浏览器
            try:
                self.browser.quit()
            except:
                pass


if __name__ == '__main__':
    spider = Spider()
    spider.main()