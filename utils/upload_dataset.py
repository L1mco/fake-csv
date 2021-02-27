def upload_instance(instance, filename):

    return 'uploads/%s/%s/%s' % (
        instance.schema.owner.id,
        instance.created_date,
        filename
    )
