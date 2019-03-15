import graphene

from graphene_django import DjangoObjectType

from lists.models import Item


class ItemType(DjangoObjectType):
    class Meta:
        model = Item


class Query(graphene.ObjectType):
    items = graphene.List(ItemType)
    item = graphene.Field(ItemType, item_id=graphene.Int(required=True))
    foo_foo = 'Foo'

    def resolve_items(self, info, **kwargs):
        user = info.context.user
        if not user.is_anonymous:
            return Item.objects.all()
        raise Exception('Not logged in')

    def resolve_item(self, info, item_id):
        return Item.objects.get(pk=item_id)


class ItemCreate(graphene.Mutation):
    item = graphene.Field(ItemType)

    class Arguments:
        text = graphene.String(required=True)
        done = graphene.Boolean()

    def mutate(self, info, text, **kwargs):
        item = Item.objects.create(text=text, **kwargs)
        return ItemCreate(item=item)


class ItemUpdate(graphene.Mutation):
    item = graphene.Field(ItemType)

    class Arguments:
        item_id = graphene.Int(required=True)
        text = graphene.String()
        done = graphene.Boolean()

    def mutate(self, info, item_id, **kwargs):
        qs = Item.objects.filter(pk=item_id)
        qs.update(**kwargs)
        return ItemUpdate(item=qs[0])


class ItemDelete(graphene.Mutation):
    item_id = graphene.Int()

    class Arguments:
        item_id = graphene.Int(required=True)

    def mutate(self, info, item_id):
        Item.objects.get(pk=item_id).delete()
        return ItemDelete(item_id=item_id)


class Mutation(graphene.ObjectType):

    item_create = ItemCreate.Field()
    item_update = ItemUpdate.Field()
    item_delete = ItemDelete.Field()
