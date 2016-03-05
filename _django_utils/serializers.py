from rest_framework import serializers


def as_money(num, precision=0.01):
    if num is None:
        return None
    return round(num / precision) * precision


class MagicModelSerializer(serializers.ModelSerializer):
    """ModelSerializer with 'Meta.exclude_fields', 'Meta.renamed_fields' properties."""

    def __init__(self, model=None, exclude_fields=None, rename_fields=None, *args, **kwargs):
        self.exclude_fields = exclude_fields or getattr(self.Meta, 'exclude_fields', [])
        self.rename_fields = rename_fields or getattr(self.Meta, 'rename_fields', dict())
        return super(MagicModelSerializer, self).__init__(model, *args, **kwargs)

    def get_fields(self):
        fields = super(MagicModelSerializer, self).get_fields()

        try:
            # Removing fields
            for exclude_field_name in self.exclude_fields:
                fields.pop(exclude_field_name)

            # Renaming fields
            for field_name, new_field_name in self.rename_fields.items():
                fields[new_field_name] = fields.pop(field_name)
        except KeyError as ke:
            raise KeyError("%s not found; select from %s" % (ke.message, list(fields.keys())))
        return fields
