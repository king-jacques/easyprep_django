from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.db import transaction, models
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import xlwt
import csv
import uuid
import datetime

from rest_framework.utils.serializer_helpers import ReturnList
import requests
from django.core.files.base import ContentFile
import os
from django.apps import apps
import zipfile
from django.core.files.storage import default_storage
from io import BytesIO
from utils.serializers import GenericSerializer
import json
from .utils import is_guid
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from rest_framework.serializers import BaseSerializer





class ExportData:

    renamed_fields = {
        "nme": "Name",
        "Usr": "User",
        "Ordr": "Order",
    }   

    default_excluded_fields = ["guid_id", "assessmentdatetime"]

    content_types = {
        "txt": "text/plain",
        "csv": "text/csv",
        "xls": "application/vnd.ms-excel",
        "json": "application/json",
        "xlsx": 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    def __init__(self, queryset:dict, selected:dict=None, exclude=None, path=None, filename=None):
        if type(queryset) != dict:
            raise Exception('Queryset must be a dict instance')
        self.queryset = []
        self.sheets = []
        self.models = {}
        counter = 0
        for sheet_name, data in queryset.items():
            counter +=1
            if hasattr(data, 'model'):
                model = data.model
            elif isinstance(data, ReturnList):
                #allow support for serializer data
                model = None
            elif isinstance(data, list):
                model = data[0].__class__ #type(data[0])
            
            else:
                raise Exception('must be queryset, or list')
            
            model_name = model.__name__ if model else f'DictItem{counter}'
            self.queryset.append(data)
            self.sheets.append((sheet_name, model_name))
            if model_name in self.models:
                continue
            if type(model) == ModelBase:
                model_fields = model._meta.fields
                fields = [field.name for field in model_fields if field.name not in self.default_excluded_fields]
            elif not model:
                #This is a dict:
                print('DATA', data)
                if data:
                    fields = list(data[0].keys())

            else:
                fields = [attr for attr,_ in data[0].__dict__.items() if not self.is_private_attr(attr) and attr not in self.default_excluded_fields]
            self.models[model_name] = fields
        
        if exclude:
            self.default_excluded_fields.extend(exclude)
        
        self.get_fields(selected)
        self.get_column_names()
        self.filename = filename

    def get_fields(self, selected):
        #selected should be a dictionary with the sheetnames and fields to write.
        if selected:
            if type(selected) != dict:
                raise Exception('selected must be a dict instance with key of sheetname and values containing an iterable of fields to write')
            
            for model_name,fields in selected.items():
                if model_name in self.models:
                    selected_fields = [field for field in fields if field in self.models[model_name]]
                    self.models[model_name] = selected_fields
    
    def get_column_names(self):
        # #column names for fields that will be written to the excel sheet
        column_names = {}
        for model, fields in self.models.items():
            field_list = [self.renamed_fields[field] if field in self.renamed_fields else field.capitalize() for field in fields]
            column_names[model] = field_list
        self.column_names = column_names

    def get_formatted_response(self, format):
        response = HttpResponse(content_type=self.content_types[format])
        filename = f'ResearchData{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'
        response['Content-Disposition'] = f'attachment; filename="{self.filename or filename}.{format}"'
        return response
    
    def parse_int(self, string):
        if isinstance(string, int) or isinstance(string, float):
            return string
        else:
            return str(string)

    def excel_writer(self):
        wb = xlwt.Workbook(encoding='utf-8')

        for sheet in range(len(self.queryset)):
            #add sheet
            model_name = self.sheets[sheet][1]
            #column_names = self.column_names[model_name]
            column_names = self.models[model_name]
            #column_names = self.column_names[sheet][1]
            ws = wb.add_sheet(f'{self.sheets[sheet][0]}') #

            #sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            
            #write column names
            for col_num in range(len(column_names)):
                ws.write(row_num, col_num, str(column_names[col_num]), font_style) #start at 0 row 0 column

            #sheetbody remaining rows
            font_style = xlwt.XFStyle()
            rows = self.get_values_list(sheet) #
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    #cast to str incase of UUID
                    ws.write(row_num, col_num, self.parse_int(row[col_num]), font_style)
        return wb
    
    def export_as_excel(self, path=None):
        file = self.excel_writer()
        if path:
            file.save(path)
            print(f'file saved to {path}')
            return
        response = self.get_formatted_response('xls')
        file.save(response)
        return response
        
    def export_as_format(self, format):
        if format not in self.content_types:
            format = "csv"
        
        if format == "csv":
            return self.export_as_csv()
        elif format == "xls":
            return self.export_as_excel()
        
    def get_values_list(self, sheet=None):
        def get_sheet_values(sheet):
            if isinstance(self.queryset[sheet], QuerySet):
                model_name = self.sheets[sheet][1]
                return self.queryset[sheet].values_list(*self.models[model_name])
            elif isinstance(self.queryset[sheet], ReturnList):
                values_list = []
                for item in self.queryset[sheet]:
                    if item is not None:
                        item_list = []
                        for attr,val in item.items():
                            if not self.is_private_attr(attr):
                                item_list.append(val)
                        values_list.append(item_list)
                return values_list
                
            else:
                values_list = []
                for item in self.queryset[sheet]:
                    if item is not None:
                        item_list = []
                        for attr,val in item.__dict__.items():
                            if not self.is_private_attr(attr):
                                item_list.append(val)
                        values_list.append(item_list)
                return values_list
            
        if sheet is not None:
            return get_sheet_values(sheet)
        else:
            #csv file, concatenate all values.
            values_list = []
            for sheet in range(len(self.queryset)):
                values_list.extend(get_sheet_values(sheet))
            return values_list
        
    def is_private_attr(self, attr):
        return attr[0] == '_'
    
    def export_as_csv(self, path=None):
        if path:
            with open(path, 'w', newline='') as csv_file:
                self.csv_writer(csv_file)
                print(f'file saved to {path}')
            return
        response = self.get_formatted_response('csv')
        self.csv_writer(response)
        return response

    def csv_writer(self, file):
        if len(self.models) != 1:
            raise Exception('cannot export multiple models to csv. use xls')
        column_names = list(self.column_names.values())[0]
        writer = csv.writer(file)
        writer.writerow(column_names)
        csv_content = self.get_values_list()
        for row in csv_content:
            writer.writerow(row)
    

class ImportExcelData:
    failed_keys = {}
    current_sheet = None
    guids = {}
    cache = {}
    many_to_many = None
    def __init__(self, path, replace_guids = False, models:dict=None, rename_duplicates:dict=None, bulk_create=True):
        '''
            Import Excel Data
            Assumes a multi sheet excel file.
            Params:
            * replace_guids: create new guids for objects
            * models: specifies what model to use for each sheet name e.g {'organization': OrganisationUnit} indicates to use the model OrganisationUnit for the sheet with title 'organization'
            * rename_duplicates: specifies what models should be renamed if they are duplicates and what fields on the model should be renamed. e.g {'TrainingPlan': 'name'} indicates that if a Training Plan having the same name already exists, add - copy to the name.
        '''
        sheets = pd.read_excel(path, sheet_name=None)
        for sheet_name, df in sheets.items():
            sheets[sheet_name] = df.fillna('') #replace Nan with empty string
            if 'guid' in df.columns and replace_guids:
                sheets[sheet_name]['guid'] = sheets[sheet_name]['guid'].apply(self.replace_guid)
            if 'id' in df.columns:
                sheets[sheet_name]['id'] = sheets[sheet_name]['id'].apply(lambda x: 'None')
        self.sheets = sheets
        if models:
            self.models |= models
        self.duplicates = rename_duplicates
        self.bulk_create = bulk_create

    models = {'TrainingPlan': TrainingPlan, 'TpCycle': TpCycle, 'TpWorkout': TpWorkout}
        
    def load_to_db(self):
        with transaction.atomic():
            for sheet_name, df in self.sheets.items():
                num_rows = df.shape[0]
                
                print(f"Loading {sheet_name}...")
                self.current_sheet = sheet_name
                if sheet_name in self.models:
                    model = self.models[sheet_name]
                    items = []
                    raw_data = []
                    for index, row in df.iterrows():
                        self.many_to_many = []
                        self.has_file = []
                        if index % 100 == 0:
                            print(f'\nloading item {index + 1}/{num_rows}')
                        row_dict = row.to_dict()
                        rows = self.get_valid_rows(row_dict)
                        rows = self.deserialize(model, rows)
                        if self.bulk_create:
                            item = model(**rows)
                        else:
                            item = rows
                        if self.has_file:
                            if self.bulk_create:
                                for file in self.has_file:
                                    field_name, file_name, content = file
                                    file_field = getattr(item, field_name)
                                    file_field.save(file_name, content, save=False)
                            else:
                                for file in self.has_file:
                                    field_name, file_name, content = file
                                    item[field_name] = content
                        if model == TrainingPlan:
                            while TrainingPlan.objects.filter(name=item.name).exists():
                                if self.bulk_create:
                                    item.name = item.name + ' - Copy'
                                else:
                                    item['name'] = item['name'] + ' - Copy'
                        elif self.duplicates and model.__name__ in self.duplicates:
                            item = self.check_duplicates(model, self.duplicates[model.__name__], item)

                        # Check here if this field has many to many
                        if not self.many_to_many:
                            items.append(item) #append for bulk create later
                        else:
                            #create immediately
                            instance = model.objects.create(**rows)
                            #instance = item.save()
                            for related_objs in self.many_to_many:
                                related_model = related_objs[0]
                                field = related_objs[1]
                                field_value = related_objs[2]
                                if field_value:
                                    values_list = [field.strip() for field in field_value.split(",")]
                                    if values_list:
                                        related_instances = related_model.objects.filter(pk__in=values_list) # TODO check that values_list is valid
                                    getattr(instance, field).set(related_instances)
                    if self.bulk_create:
                        print("bulk creating items...")
                        model.objects.bulk_create(items)
                    else:
                        for item in items:
                            print('creating items...')
                            model.objects.create(**item)
                    print('updating foreign keys', sheet_name)
                    self.update_foreign_keys(model, sheet_name)
    
    def deserialize(self, model, row_data):
        deserialized_json = {}
        for field_name, field_value in row_data.items():
            field = model._meta.get_field(field_name)
            if isinstance(field, models.ManyToManyField):
                related_model = field.related_model
                if field_value:
                    self.many_to_many.append((related_model, field_name, field_value))
            elif isinstance(field, models.ForeignKey):
                related_model = field.related_model
                try:
                    related_instance = self.get_cache_obj(related_model, field_value)
                    deserialized_json[field_name] = related_instance
                except related_model.DoesNotExist:
                    deserialized_json[field_name] = None #this object might not have been created yet so let's make it None for now.
                    print('@', end='')
                    self.register_failed_key(field.name, field_value) #save this info so that we can update this object later
            elif isinstance(field, models.IntegerField):
                deserialized_json[field_name] =int(field_value)
            elif isinstance(field, models.BooleanField):
                deserialized_json[field_name] = True if field_value == 'True' or 'TRUE' else False
            elif isinstance(field, models.UUIDField):
                deserialized_json[field_name] = uuid.UUID(field_value)

            elif isinstance(field, models.ImageField) or isinstance(field, models.FileField):
                if field_value:
                    try:
                        response = requests.get(field_value)
                        if response.status_code == 200:
                            file_name = os.path.basename(field_value) #field_value.split("/")[-1] #last part with extension os.path.basename(field_value)
                            content = ContentFile(response.content)
                            self.has_file.append((field_name, file_name, content))
                        else:
                            #
                            print(f"could not load file from: {field_value}")
                    except:
                        print(f"could not load file from: {field_value}")
                    
            else:
                deserialized_json[field_name] = field_value
        return deserialized_json

    def register_failed_key(self, field_name, value):
        current_sheet = self.current_sheet
        if current_sheet:
            if current_sheet in self.failed_keys:
                if field_name in self.failed_keys[current_sheet]:
                    self.failed_keys[current_sheet][field_name].append(value)
                else:
                    self.failed_keys[current_sheet][field_name] = [value]
            else:
                self.failed_keys[current_sheet] = {field_name: [value]}

    def update_foreign_keys(self, model, sheet_name):
        '''
        This is to update self referential foreign keys, as the objects might not have been created at the point of calling load_to_db
        '''
        if sheet_name not in self.failed_keys:
            return
        fields = list(self.failed_keys[sheet_name].keys())
        values = []
        for field in fields:
            values.extend(self.failed_keys[sheet_name][field])
        model_fields = model._meta.get_fields()
        if fields:
            model_fields = [field for field in model_fields if field.name in fields]
        foreign_keys = [field for field in model_fields if isinstance(field, models.ForeignKey)]
        df = self.sheets[sheet_name]
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            rows = self.get_valid_rows(row_dict)
            guid = rows.get('guid')
            for field in foreign_keys:
                related_model = field.related_model
                field_value=rows.get(field.name)
                if field_value is not None and field_value in values:
                    try:
                        instance = model.objects.get(guid=guid) #object should exist we just created it
                    except ObjectDoesNotExist:
                        continue
                    try:
                        related_instance  = self.get_cache_obj(related_model, field_value)
                        setattr(instance, field.name, related_instance)
                        print(f"Updating {instance}'s {field.name} with {related_instance}")
                        instance.save()
                    except related_model.DoesNotExist:
                        print('Object does not exist', field.name, field_value, guid)

    def get_valid_rows(self, rows):
        valid_rows = {field: self.guids[value] if value in self.guids else value for field, value in rows.items() if value != 'None'}

        return valid_rows
    
    def replace_guid(self, string):
        try:
            g = uuid.UUID(string)
            if string in self.guids:
                #we've seen this guid before.
                return self.guids[string]
            else:
                #seeing this guid for the first time. generate new guid and hash it
                new_guid = str(uuid.uuid4())
                self.guids[string] = new_guid
                return new_guid
        except:
            return string
        
    def get_cache_obj(self, model, guid):
        model_name = model.__name__
        if model_name not in self.cache:
            self.cache[model_name] = {}
        elif guid in self.cache[model_name]:
            obj = self.cache[model_name][guid]
            print('#', end='')
            return obj
        
        obj = model.objects.get(pk=guid)
        print('.', end='')
        self.cache[model_name][guid] = obj
        return obj
    
    def check_duplicates(self, model, key, item):
        if hasattr(item, key) and isinstance(getattr(item, key), str):
            while model.objects.filter(**{key: getattr(item, key)}).exists():
                new_key = f"{getattr(item, key)} - Copy"
                setattr(item, key, new_key)
        return item

class ImportExportZip:
    def __init__(self, queryset, filename=None):
        self.queryset = queryset
        self.filename = filename or f'model_data{datetime.now().strftime("%B %d")}'

    @staticmethod
    def write_file_fields(zip_file, queryset, file_fields_names):
        for instance in queryset:
            for field in file_fields_names:
                file_field = getattr(instance, field)
                if file_field:
                    file_path = file_field.url.lstrip('/')
                    try:
                        with default_storage.open(file_field.name, 'rb') as file: # Open the file that we want to write
                            zip_file.writestr(file_path, file.read()) # Write file to zip
                    except:
                        pass
    @staticmethod
    def zip_queryset(sheets:list):
        ''' takes a list of tuples. where each tuple contains the queryset/instance and a boolean of whether to include many to many fields
            e.g [(organizations, True), (subscriptions, False)]        
        '''
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for queryset, many_to_many, *rest in sheets:
                if isinstance(queryset, BaseSerializer):
                    # Special case for serializer
                    serializer = queryset
                    queryset = serializer.instance
                    queryset = queryset if hasattr(serializer, 'many') else (queryset,)
                    model = serializer.child.Meta.model if hasattr(serializer, 'many') else serializer.Meta.model
                    data = serializer.data
                    if data:
                        data_to_write = data if hasattr(serializer, 'many') else [data]
                else:
                    exclude = rest[0] if rest else []
                    serializer = GenericSerializer(queryset, exclude=exclude, stringify=True, many_to_many=many_to_many, concat_many_to_many=many_to_many )
                    model = serializer.model
                    queryset = (queryset,) if not serializer.many else queryset
                    data = serializer.data
                    if data:
                        data_to_write = data if serializer.many else [data]
                
                model_name = model.__name__
                model_path = f"{model._meta.app_label}.{model_name}"
                
                

                zip_file.writestr(f"models/{model_path}.json", json.dumps(data_to_write))
                
                fields = model._meta.fields
                file_fields_names = [field.name for field in fields if isinstance(field, models.FileField) or isinstance(field, models.ImageField)]
                ImportExportZip.write_file_fields(zip_file, queryset, file_fields_names)
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    @staticmethod
    def unzip(zip_file_content, update_created=True, replace_guids=True):
        guids = {}
        def replace_guid(string):
            try:
                g = uuid.UUID(string)
                if string in guids:
                    return guids[string]
                else:
                    return string
            except:
                return string
        
        replace_with_slug = ['subscription', 'subscriptionguid', 'subscription_type',] # 'assessment_questionnaire', 'workout_questionnaire'
        zip_buffer = BytesIO(zip_file_content)
        with transaction.atomic():
            with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
                for file_info in zip_file.infolist():
                    if file_info.is_dir():
                        continue 
                    file_name = file_info.filename
                    if file_name.startswith('models/') and file_name.endswith('.json'):
                        model_path = file_name.removesuffix('.json').split('/')[1]
                        app_label, model_name = model_path.split('.')
                        model_class = apps.get_model(app_label, model_name)
                        with zip_file.open(file_info) as json_file:
                            data = json.load(json_file)
                            file_fields_names = [field.name for field in model_class._meta.fields if isinstance(field, models.FileField) or isinstance(field, models.ImageField)]
                            today = now()
                            pk_field = model_class._meta.pk.name
                            new_data = []
                            for item in data:
                                for field in file_fields_names:
                                    file_url = item.get(field)
                                    if file_url:
                                        file_url = file_url.lstrip('/')
                                        try:
                                            with zip_file.open(file_url) as media_file:
                                                file_name = os.path.basename(file_url)
                                                item[field] = ContentFile(media_file.read(),name=file_name)
                                        except Exception as e:
                                            item[field] = None
                                if update_created:
                                    item['created'] = today
                                    item['modified'] = today

                                if replace_guids:
                                    old_guid = item.get('guid')
                                    if old_guid:
                                        #replace guids
                                        new_guid = str(uuid.uuid4())
                                        guids[old_guid] = str(new_guid)
                                
                                    new_item = {key: replace_guid(value) for key, value in item.items()}
                                else:
                                    new_item = item

                                if 'id' in new_item:
                                    new_item.pop('id')

                                if 'training_plan_override' in new_item:
                                    training_plan_override = new_item['training_plan_override']
                                    if training_plan_override:
                                        training_plan_override = training_plan_override.split(", ")
                                        new_item['training_plan_override'] = training_plan_override
                                    else:
                                        new_item['training_plan_override'] = []
                                        
                                # Fix to use subscription slugs instead of guids
                                keys_to_replace = [field for field in replace_with_slug if field in new_item]
                                if keys_to_replace:
                                    for key in keys_to_replace:
                                        value = new_item[key]
                                        if not is_guid(value): # if we have a subscription field but the value is not a guid its most likely a slug
                                            # Use slug instead
                                            try:
                                                sub = SubscriptionType.objects.get(slug=value)
                                                sub = sub.guid
                                            except:
                                                sub = None
                                            new_item[key] = sub
                                new_data.append(new_item)




                            SerializerClass = GenericSerializer.model_serializer(model_class, many_to_many=True) 
                            serializer = SerializerClass(data=new_data, many=True)
                            
                            if serializer.is_valid(): # TODO this takes about 8s
                                serializer.save() # TODO this takes about 20s
                            else:
                                raise ValidationError(serializer.errors)

    def zip(self):
        return self.zip_queryset(self.queryset)
    
    def get_response(self):
        zip_buffer = self.zip()
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={self.filename}.zip'
        return response
    
 