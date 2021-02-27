def upload_instance(instance, filename):

    return 'uploads/%s/%s/%s' % (
        instance.schema.owner.username,
        instance.created_date,
        filename
    )
