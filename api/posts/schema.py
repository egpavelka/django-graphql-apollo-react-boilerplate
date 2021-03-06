import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from users.schema import UserType
from .models import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class Query(graphene.ObjectType):
    post = graphene.Field(PostType, id=graphene.ID())
    posts = graphene.List(PostType, author=graphene.ID())

    def resolve_post(self, info, id):
        return Post.objects.get(id=id)

    def resolve_posts(self, info, author=None, **kwargs):
        if author:
            return Post.objects.filter(author=author)

        return Post.objects.all()



class CreatePost(graphene.Mutation):
    id = graphene.Int()
    text = graphene.String()
    author = graphene.Field(UserType)

    class Arguments:
        text = graphene.String()

    @login_required
    def mutate(self, info, text):
        user = info.context.user or None

        post = Post(
            text=text,
            author=user
        )
        post.save()

        return CreatePost(
            id=post.id,
            text=post.text,
            author=post.author
        )


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
