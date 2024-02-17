import graphene


class AddressInput(graphene.InputObjectType):
    address1 = graphene.String(required=True)
    address2 = graphene.String()
    city = graphene.String(required=True)
    state = graphene.String(required=True)
    country = graphene.String(required=True)
    postal_code = graphene.String(required=True)


class ContactInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=True)
