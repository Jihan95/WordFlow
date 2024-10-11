from faker import Faker
from models.engine import db_storage
from models.user import User
from models.post import Post
from models.comment import Comment
from models.category import Category
from models.tag import Tag

fake = Faker()

# Get the storage instance
storage = db_storage.DBStorage()
storage.reload()

def create_users(n):
    users = []
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password_hash = fake.password()  # You should use proper hashing
        user = User(username=username, email=email, password_hash=password_hash)
        users.append(user)
        storage.new(user)
    storage.save()
    return users

def create_categories(n):
    categories = []
    for _ in range(n):
        name = fake.word()
        category = Category(name=name)
        categories.append(category)
        storage.new(category)
    storage.save()
    return categories

def create_posts(users, categories, n):
    posts = []
    for _ in range(n):
        title = fake.sentence()
        content = fake.text()
        user = fake.random_element(users)
        category = fake.random_element(categories)
        post = Post(title=title, content=content, user_id=user.id, category_id=category.id)
        posts.append(post)
        storage.new(post)
    storage.save()
    return posts

def create_comments(users, posts, n):
    comments = []
    for _ in range(n):
        content = fake.text()
        user = fake.random_element(users)
        post = fake.random_element(posts)
        comment = Comment(content=content, user_id=user.id, post_id=post.id)
        comments.append(comment)
        storage.new(comment)
    storage.save()
    return comments

if __name__ == "__main__":
    # Create fake data for testing
    print("Creating users...")
    users = create_users(10)

    print("Creating categories...")
    categories = create_categories(5)

    print("Creating posts...")
    posts = create_posts(users, categories, 20)

    print("Creating comments...")
    comments = create_comments(users, posts, 50)

    print("Fake data successfully inserted into the database!")
