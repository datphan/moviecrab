# -*- coding: utf-8 -*-
#http://stackoverflow.com/questions/16319250/using-flask-admin-how-can-i-get-a-tag-field-supporting-un-existed-tags
#https://codeseekah.com/2013/08/04/flask-admin-hacks-for-many-to-many-relationships/
from .models import Episode, Movie
from ..genre.models import Genre
from ..people.models import People
from ..country.models import Country
from ..tag.models import Tag

from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.form import InlineModelConverter
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.form.widgets import Select2Widget, Select2TagsWidget
from flask_admin.form import Select2Field, Select2TagsField
from wtforms import TextAreaField
from wtforms.widgets import TextArea


# class InlineModelConverter(InlineModelConverterBase):
#     """
#         Inline model form helper.
#     """

#     inline_field_list_type = InlineModelFormList
#     """
#         Used field list type.

#         If you want to do some custom rendering of inline field lists,
#         you can create your own wtforms field and use it instead
#     """

#     def __init__(self, session, view, model_converter):
#         """
#             Constructor.

#             :param session:
#                 SQLAlchemy session
#             :param view:
#                 Flask-Admin view object
#             :param model_converter:
#                 Model converter class. Will be automatically instantiated with
#                 appropriate `InlineFormAdmin` instance.
#         """
#         super(InlineModelConverter, self).__init__(view)
#         self.session = session
#         self.model_converter = model_converter

#     def get_info(self, p):
#         info = super(InlineModelConverter, self).get_info(p)

#         # Special case for model instances
#         if info is None:
#             if hasattr(p, '_sa_class_manager'):
#                 return self.form_admin_class(p)
#             else:
#                 model = getattr(p, 'model', None)

#                 if model is None:
#                     raise Exception('Unknown inline model admin: %s' % repr(p))

#                 attrs = dict()
#                 for attr in dir(p):
#                     if not attr.startswith('_') and attr != 'model':
#                         attrs[attr] = getattr(p, attr)

#                 return self.form_admin_class(model, **attrs)

#             info = self.form_admin_class(model, **attrs)

#         # Resolve AJAX FKs
#         info._form_ajax_refs = self.process_ajax_refs(info)

#         return info

#     def process_ajax_refs(self, info):
#         refs = getattr(info, 'form_ajax_refs', None)

#         result = {}

#         if refs:
#             for name, opts in iteritems(refs):
#                 new_name = '%s-%s' % (info.model.__name__.lower(), name)

#                 loader = None
#                 if isinstance(opts, dict):
#                     loader = create_ajax_loader(info.model, self.session, new_name, name, opts)
#                 else:
#                     loader = opts

#                 result[name] = loader
#                 self.view._form_ajax_refs[new_name] = loader

#         return result

#     def contribute(self, model, form_class, inline_model):
#         """
#             Generate form fields for inline forms and contribute them to
#             the `form_class`

#             :param converter:
#                 ModelConverterBase instance
#             :param session:
#                 SQLAlchemy session
#             :param model:
#                 Model class
#             :param form_class:
#                 Form to add properties to
#             :param inline_model:
#                 Inline model. Can be one of:

#                  - ``tuple``, first value is related model instance,
#                  second is dictionary with options
#                  - ``InlineFormAdmin`` instance
#                  - Model class

#             :return:
#                 Form class
#         """

#         mapper = model._sa_class_manager.mapper
#         info = self.get_info(inline_model)

#         # Find property from target model to current model
#         target_mapper = info.model._sa_class_manager.mapper

#         reverse_prop = None

#         for prop in target_mapper.iterate_properties:
#             if hasattr(prop, 'direction') and prop.direction.name in ('MANYTOONE', 'MANYTOMANY'):
#                 if issubclass(model, prop.mapper.class_):
#                     reverse_prop = prop
#                     break
#         else:
#             raise Exception('Cannot find reverse relation for model %s' % info.model)

#         # Find forward property
#         forward_prop = None

#         if prop.direction.name == 'MANYTOONE':
#             candidate = 'ONETOMANY'
#         else:
#             candidate = 'MANYTOMANY'

#         for prop in mapper.iterate_properties:
#             if hasattr(prop, 'direction') and prop.direction.name == candidate:
#                 if prop.mapper.class_ == target_mapper.class_:
#                     forward_prop = prop
#                     break
#         else:
#             raise Exception('Cannot find forward relation for model %s' % info.model)

#         # Remove reverse property from the list
#         ignore = [reverse_prop.key]

#         if info.form_excluded_columns:
#             exclude = ignore + list(info.form_excluded_columns)
#         else:
#             exclude = ignore

#         # Create converter
#         converter = self.model_converter(self.session, info)

#         # Create form
#         child_form = info.get_form()

#         if child_form is None:
#             child_form = get_form(info.model,
#                                   converter,
#                                   base_class=info.form_base_class or form.BaseForm,
#                                   only=info.form_columns,
#                                   exclude=exclude,
#                                   field_args=info.form_args,
#                                   hidden_pk=True,
#                                   extra_fields=info.form_extra_fields)

#         # Post-process form
#         child_form = info.postprocess_form(child_form)

#         kwargs = dict()

#         label = self.get_label(info, forward_prop.key)
#         if label:
#             kwargs['label'] = label

#         if self.view.form_args:
#             field_args = self.view.form_args.get(forward_prop.key, {})
#             kwargs.update(**field_args)

#         # Contribute field
#         setattr(form_class,
#                 forward_prop.key,
#                 self.inline_field_list_type(child_form,
#                                             self.session,
#                                             info.model,
#                                             reverse_prop.key,
#                                             info,
#                                             **kwargs))

#         return form_class


class PostModelViewInlineModelConverter(InlineModelConverter):
    def contribute(self, model, form_class, inline_model):
        mapper = object_mapper( model() )
        target_mapper = object_mapper( inline_model() )

        info = self.get_info( inline_model )

        # Find reverse property
        for prop in target_mapper.iterate_properties:
            if hasattr( prop, 'direction' ) and prop.direction.name == 'MANYTOMANY':
                if issubclass( model, prop.mapper.class_ ):
                    reverse_prop = prop
                    break
        else:
            raise Exception( 'Cannot find reverse relation for model %s' % info.model )

        # Find forward property
        for prop in mapper.iterate_properties:
            if hasattr( prop, 'direction' ) and prop.direction.name == 'MANYTOMANY':
                if prop.mapper.class_ == target_mapper.class_:
                    forward_prop = prop
                    break
        else:
            raise Exception( 'Cannot find forward relation for model %s' % info.model )
        child_form = info.get_form()
        if child_form is None:
            child_form = get_form(
                info.model,
                only=PostModelView.form_columns,
                exclude=PostModelView.form_excluded_columns,
                field_args=PostModelView.form_args,
                hidden_pk=True
            )
        child_form = info.postprocess_form( child_form )

        setattr( form_class, forward_prop.key + '_add', self.inline_field_list_type(
            child_form, self.session, info.model, reverse_prop.key, info
        ) )

        return form_class

from ..extensions import db

class MovieAdminView(ModelView):
    inline_models = (Episode, )

    form_choices = {
        'type': Movie.TYPES,
        'quality': Movie.QUALITIES
    }

    # form_ajax_refs = {
    #     'tags': {
    #         'fields': ('name', ),
    #         'page_size': 10
    #     },
    #     # 'tags_add': QueryAjaxModelLoader('tags', db.session, Movie, fields=['name'], page_size=10),
        
    # }

    # form_excluded_columns = ('tags', )

    # form_extra_fields = {
    #     'tags_add': Select2TagsField('Tags', data=QueryAjaxModelLoader('tags', db.session, Movie, fields=['name'], page_size=10))
    # }

    # inline_model_form_converter = PostModelViewInlineModelConverter

    # def on_model_change(self, form, model, is_created):
    #     form.tags_add.populate_obj( model, 'tags' )
    #     self.session.add( model )


    # form_ajax_refs = {
    #     'genres': {
    #         'fields': (Genre.name, )
    #     },
    #     'actors': {
    #         'fields': (People.name, )
    #     },
    #     'directors': {
    #         'fields': (People.name, )
    #     },
    #     'countries': {
    #         'fields': (Country.name, )
    #     },
    # }

    # def scaffold_form(self):
    #     form_class = super(MovieAdminView, self).scaffold_form()
    #     form_class.extra = fields.QuerySelectField(Genre.name)
    #     return form_class