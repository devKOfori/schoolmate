def create_block(klass):
    block = klass.objects.create(
        hostel=self, name="Default Block", createdby=self.createdby
    )
    return block
