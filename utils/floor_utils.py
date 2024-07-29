def create_floor(model, block, created_by):
    floor = model.objects.create(
        block=block, name="Default Floor", createdby=created_by
    )
    return floor
