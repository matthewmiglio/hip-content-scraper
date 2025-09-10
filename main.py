from modules.reddit import RedditScraper

def main():
    reddit_posts = []
    reddit_scraper = RedditScraper()
    target_reddit_threads = [
        r'https://www.reddit.com/r/lovable/',
        r'https://www.reddit.com/r/DigitalMarketing/',
        # r'https://www.reddit.com/r/webdev/',
        # r'https://www.reddit.com/r/ArtificialInteligence',
        # r'https://www.reddit.com/r/ChatGPT',
        # r'https://www.reddit.com/r/technology',
    ]
    for target_reddit_thread in target_reddit_threads:
        post_links = reddit_scraper.get_posts(target_reddit_thread, max_posts=3, scroll_pause=0.2, max_scrolls=200)
        posts = [reddit_scraper.get_post_content(post_link) for post_link in post_links]
        reddit_posts.extend(posts)

    print(f'Have {len(reddit_posts)} reddit posts from {len(target_reddit_threads)} threads')


if __name__ == '__main__':
    main()