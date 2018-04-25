from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from xiaoi_ops import settings
from cmdb.models import cmdb
from django.urls import reverse_lazy
from .form import CmdbForm,FileForm
import json,csv,codecs,chardet
from io import StringIO

from django.db.models import Q
# Create your views here.
class CmdbListAll(LoginRequiredMixin,ListView):
    template_name = 'cmdb/cmdb.html'
    paginate_by = settings.DISPLAY_PER_PAGE
    model = cmdb
    context_object_name = "cmdb_list"
    ordering = ("id")

    def get_queryset(self):
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            queryset =super().get_queryset().filter(
                Q(network_ip=query) | Q(hostname=query) | Q(inner_ip=query) | Q(project=query) | Q(
                    manager=query)).order_by('-id')
        else:
            queryset = super().get_queryset()
        return queryset





class CmdbAdd(LoginRequiredMixin, CreateView):
    """资产增加"""
    model = cmdb
    form_class = CmdbForm
    template_name = 'cmdb/cmdb-add-update.html'
    success_url = reverse_lazy('cmdb:cmdb_list')

class CmdbUpdate(LoginRequiredMixin,UpdateView):
    model = cmdb
    form_class = CmdbForm
    template_name = 'cmdb/cmdb-add-update.html'
    success_url = reverse_lazy('cmdb:cmdb_list')

class CmdbDetail(LoginRequiredMixin, DetailView):
    model = cmdb
    template_name = 'cmdb/cmdb-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg,None)
        detail = cmdb.objects.get(id=pk)
        text = {
            "nid":pk,
            "detail":detail
        }
        kwargs.update(text)
        return super().get_context_data(**kwargs)


class CmdbDel(LoginRequiredMixin,View):
    model = cmdb
    def post(self,request):
        ret = {'status':True,'error':None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid',None)
                cmdb.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id',None)
                if len(ids) == 0:
                    ret['status'] = False
                    ret['error'] = '请选者删除的条目'
                else:
                    idstring = ','.join(ids)
                    cmdb.objects.extra(where=['id IN ('+ idstring+')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除错误'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


class CmdbExport(LoginRequiredMixin,View):

    def get(self, request):

        fields = [
            field for field in cmdb._meta.fields
        ]
        print(fields)
        filename = 'assets.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response, dialect='excel', quoting=csv.QUOTE_MINIMAL)
        header = [field.verbose_name for field in fields]
        writer.writerow(header)
        cmdb_list = cmdb.objects.all()
        for cmdb_ in cmdb_list:
            data = [getattr(cmdb_, field.name) for field in fields]
            print(data)
            writer.writerow(data)

        return response

    def post(self, request):

        ids = request.POST.getlist('id', None)
        idstring = ','.join(ids)
        qs = cmdb.objects.extra(where=['id IN (' + idstring + ')']).all()

        # return  render_to_csv_response(qs)
        fields = [
            field for field in cmdb._meta.fields]
        filename = 'assets.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        response.write(codecs.BOM_UTF8)

        writer = csv.writer(response, dialect='excel', quoting=csv.QUOTE_MINIMAL)

        header = [field.verbose_name for field in fields]
        writer.writerow(header)
        for cmdb_ in qs:
            data = [getattr(cmdb_, field.name) for field in fields]
            writer.writerow(data)
        return response


@login_required
def CmdbImport(request):

    """
    资产导入

    """
    form = FileForm()
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']

            det_result = chardet.detect(f.read())
            print(det_result,codecs.BOM_UTF8.decode())
            f.seek(0)  # reset file seek index

            file_data = f.read().decode(det_result['encoding']).strip(codecs.BOM_UTF8.decode())

            csv_file = StringIO(file_data)
            reader = csv.reader(csv_file)
            csv_data = [row for row in reader]

            fields = [
                field for field in cmdb._meta.fields
            ]

            header_ = csv_data[0]
            mapping_reverse = {field.verbose_name: field.name for field in fields}
            attr = [mapping_reverse.get(n, None) for n in header_]

            created, updated, failed = [], [], []


            for row in csv_data[1:]:
                if set(row) == {''}:
                    continue
                asset_dict = dict(zip(attr, row))
                asset_dict_id = dict(zip(attr, row))
                ids = asset_dict['id']
                id_ = asset_dict.pop('id', 0)
                asset1 = cmdb.objects.filter(id=ids)  ##判断ID 是否存在

                if not asset1:
                    try:
                        if len(cmdb.objects.filter(hostname=asset_dict.get('hostname'))):
                            raise Exception(('already exists'))
                        cmdb.objects.create(**asset_dict_id)
                        created.append(asset_dict['hostname'])
                    except Exception as e:
                        failed.append('%s: %s' % (asset_dict['hostname'], str(e)))

                else:
                    for k, v in asset_dict.items():
                        if v:
                            setattr(cmdb, k, v)
                    try:
                        cmdb.objects.filter(id=ids).update(**asset_dict)
                        updated.append(asset_dict['hostname'])
                    except Exception as e:
                        failed.append('%s: %s' % (asset_dict['hostname'], str(e)))

            data = {
                'created': created,
                'created_info': 'Created {}'.format(len(created)),
                'updated': updated,
                'updated_info': 'Updated {}'.format(len(updated)),
                'failed': failed,
                'failed_info': 'Failed {}'.format(len(failed)),
                'valid': True,
                'msg': 'Created: {}. Updated: {}, Error: {}'.format(
                    len(created), len(updated), len(failed))
            }

            return render(request, 'cmdb/cmdb-import.html', {'form': form,
                                                               "msg": data})

    return render(request, 'cmdb/cmdb-import.html', {'form': form })