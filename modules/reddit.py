from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time




class Post:
    def __init__(self, username, profile_img, content, thread_name, title, url, timestamp=None):
        self.username = username
        self.profile_img = profile_img
        self.content = content
        self.thread_name = thread_name
        self.title = title
        self.url = url
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "username": self.username,
            "profile_img": self.profile_img,
            "content": self.content,
            "thread_name": self.thread_name,
            "title": self.title,
            "url": self.url,
            "timestamp": self.timestamp,
        }


class RedditScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized ")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

    def get_posts(self, thread_link, max_posts=50, scroll_pause=0.2, max_scrolls=200):
        self.driver.get(thread_link)
        time.sleep(5)

        post_links = set()
        scrolls = 0

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while len(post_links) < max_posts and scrolls < max_scrolls:
            # Scroll to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(scroll_pause)

            # Look for new posts
            posts = self.driver.find_elements(By.CSS_SELECTOR, "a.absolute.inset-0")
            for post in posts:
                href = post.get_attribute("href")
                if href and "/comments/" in href:
                    post_links.add(href)

            # Check if the scroll did anything
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # No more content
            last_height = new_height
            scrolls += 1
            print(f"Scroll {scrolls}, collected {len(post_links)} links")

        print(f"Scraped a total of {len(post_links)} post links.")
        return list(post_links)

    def url2thread_name(self, url):
        # https://www.reddit.com/r/AmItheAsshole/comments/1lu69qb/aita_for_pulling_my_daughter_from_soccer_camp_and/
        # extract the AmItheAsshole part
        try:
            thread_name = url.split("https://www.reddit.com/r/")[1].split("/")[0]
            return thread_name
        except:
            pass

        return None

    def get_post_content(self, post_link):
        print("Starting to scrape post:", post_link)
        scrape_start_time = time.time()
        print("Getting to page...")
        self.driver.get(post_link)
        time.sleep(5)

        try:
            read_more_button = self.driver.find_element(
                By.XPATH, "//button[contains(., 'Read more')]"
            )
            read_more_button.click()
            time.sleep(1)  # Let the content expand
        except:
            pass

        # repeatedly scrape content until we get all necessary data
        timeout = 10  # s
        username, profile_img, content, title, timestamp = None, None, None, None, None

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if username is None:
                    username = self.driver.find_element(
                        By.CSS_SELECTOR, "a.author-name"
                    ).text
            except:
                pass

            try:
                if profile_img is None:
                    profile_img = self.driver.find_element(
                        By.CSS_SELECTOR, "img.shreddit-subreddit-icon__icon"
                    )
            except:
                pass

            try:
                if content is None:
                    content = self.driver.find_element(By.CSS_SELECTOR, "div.md").text
            except:
                pass

            try:
                if title is None:
                    title = self.driver.find_element(
                        By.CSS_SELECTOR, "h1[id^='post-title-']"
                    ).text
            except:
                pass

            try:
                if timestamp is None:
                    timestamp_element = self.driver.find_element(
                        By.CSS_SELECTOR, "time"
                    )
                    timestamp = timestamp_element.get_attribute("datetime")
            except:
                pass

            # if all data exists break
            if None not in (username, profile_img, content, title, timestamp):
                break

        post = Post(
            username=username,
            profile_img=profile_img.get_attribute("src") if profile_img else None,
            content=content,
            thread_name=self.url2thread_name(post_link),
            title=title,
            url=post_link,
            timestamp=timestamp,
        )
        print(f"Scraped {post_link} in {time.time() - scrape_start_time:.2f}s!")
        return post


if __name__ == "__main__":
    pass