import json
import requests
import html

BC_BLOG_JSON = 'output/bc_blog_posts.json'

bc_api_url = "https://api.bigcommerce.com/stores/xxxx/v2/blog/posts?limit=200&is_published=true"

# BigCommerce API credentials
bc_access_token = "6gq07s76pi04q0calkmyt5s36qttz1e"


def run(wp_posts, bc_posts):



    i = 1
    for post in wp_posts:
        blog = get_by_title(bc_posts, post['title']['rendered'])
        # Check if blog exists on Bigcommerce
        if blog != 0:
            # update_content(blog, post)
            i = i + 1
        else:
            print(post['title'])
            #create_post(post)
            #if post["yoast_head_json"]["author"] != blog["author"]:
            #    update_author(blog, post)


def main():
    wp_posts = get_all_blogs_from_file("input/data.json")

    #bc_posts = get_all_blogs()

    bc_posts = get_all_blogs_from_file(BC_BLOG_JSON)

    for bc in bc_posts:
        print(bc["id"],",",bc['title'],",",bc["url"])

    #publish_all_posts(bc_posts)



    run(wp_posts, bc_posts)


def get_by_title(blogs, title):
    for b in blogs:
        bc_title = html.unescape(b["title"]).lower()
        wp_title = html.unescape(title).lower()

        if bc_title.strip() == wp_title.strip():
            return b

    return 0


def update_author(blog, post):
    headers = {"Accept": "application/json", "Content-Type": "application/json", "X-Auth-Token": bc_access_token}
    author = post["yoast_head_json"]["author"]
    payload = {'author': author}
    url = "https://api.bigcommerce.com/stores/421f8/v2/blog/posts/{0}"
    response = requests.put(url.format(blog["id"]), data=json.dumps(payload), headers=headers)
    print(response.status_code)


def update_content(blog, post):
    headers = {"Accept": "application/json", "Content-Type": "application/json", "X-Auth-Token": bc_access_token}
    body = post["content"]["rendered"]
    meta_description = post['yoast_head_json']['og_description']
    payload = {'body': body, 'meta_description': meta_description}
    url = "https://api.bigcommerce.com/stores/421f8/v2/blog/posts/{0}"
    response = requests.put(url.format(blog["id"]), data=json.dumps(payload), headers=headers)
    print(response.status_code)


def publish_post(blog):
    headers = {"Accept": "application/json", "Content-Type": "application/json", "X-Auth-Token": bc_access_token}
    payload = {'is_published': True}
    url = "https://api.bigcommerce.com/stores/421f8/v2/blog/posts/{0}"
    response = requests.put(url.format(blog["id"]), data=json.dumps(payload), headers=headers)
    print(response.status_code)

def create_post(post):
    headers = {"Accept": "application/json", "Content-Type": "application/json", "X-Auth-Token": bc_access_token}
    body = post["content"]["rendered"]
    meta_description = post['yoast_head_json']['og_description']
    title = html.unescape(post['title']['rendered'])
    author = post["yoast_head_json"]["author"]

    payload = {'body': body, 'meta_description': meta_description, 'title': title , 'author':author }
    url = "https://api.bigcommerce.com/stores/421f8/v2/blog/posts"
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(response.status_code)

def publish_all_posts(posts):
    for post in posts:
        publish_post(post)


def get_all_blogs():
    headers = {"Accept": "application/json", "Content-Type": "application/json", "X-Auth-Token": bc_access_token}
    response = requests.get(bc_api_url, headers=headers)
    data = response.json()
    with open(BC_BLOG_JSON, 'w') as f:
        json.dump(data, f)
    return data


def get_all_blogs_from_file(filename):
    f = open(filename)
    # returns JSON object as
    # a dictionary
    posts = json.load(f)
    return posts


if __name__ == '__main__':
    main()
