from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
import time,json

import re
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View,DetailView
from xiaoi_ops import settings
from  .models import *
from .form import AssetsForm,AssetsForm_give,AssetsForm_in
from django.core import serializers
from django.db.models import Q
from tb_log.models import tb_log
from cmdb.form import FileForm

class AssetsList(LoginRequiredMixin,ListView):
    template_name = 'assets/assets.html'
    model = assets
    context_object_name = 'assets_list'
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("active_id")


    def get_context_data(self, *, object_list=None, **kwargs):

        search_data = self.request.GET.copy()
        # print(search_data)
        try:
            search_data.pop("page")

        except BaseException as e:
            pass
        # print(search_data.dict())
        # print(search_data.urlencode())
        # context.update(search_data.dict())
        # 左侧导航站展开  "asset_active": "active",
        context = {
            "search_data": search_data.urlencode(),
            "assets_class": 'active',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)



    def get_queryset(self):
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            # print(query)
            try:
                queryset =super().get_queryset().filter(Q(user=query)|Q(uid=query)|Q(active_id=query)).order_by('active_id')
                # print('......')
            except BaseException as e:
                # print(e)
                queryset =super().get_queryset().filter(Q(user=query)|Q(uid=query)).order_by('active_id')
        else:
            queryset = super().get_queryset()
        return queryset




class AssetsAdd(LoginRequiredMixin, CreateView):
    """增加"""
    model = assets
    form_class = AssetsForm
    template_name = 'assets/assets-add-update.html'
    # success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):
        # print(self.request.POST)
        pk=request.POST['uid']
        # print(pk)
        self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'c','user':'c'})
        return super().post(request, *args, **kwargs)

class AssetsUpdateDtail(LoginRequiredMixin, UpdateView):
    model = assets
    form_class = AssetsForm
    template_name = 'assets/assets-update.html'
    context_object_name = 'obj'
    # success_url = reverse_lazy('assets:assets_list')
    def post(self, request, *args, **kwargs):
        # print(self.request.POST)
        pk=request.POST['uid']
        # print(pk)
        self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'u','user':'c'})
        return super().post(request, *args, **kwargs)

def getdata(request):
    pk = request.GET['pk']
    plat = get_object_or_404(platform, pk=pk)
    size = plat.platform_size_set.all()
    data = serializers.serialize('json', size)
    # print(data)
    return HttpResponse(data, content_type='application/json')


class AssetsDetail(LoginRequiredMixin,DetailView):
    model = assets
    template_name = 'assets/assets-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg,None)
        detail = assets.objects.get(uid=pk)
        text = {
            "detail":detail,
            "nid":pk,
        }
        kwargs.update(text)
        return super().get_context_data(**kwargs)



class AssetsUpdate(LoginRequiredMixin,UpdateView):
    '''借用和领用资产'''
    model = assets
    form_class = AssetsForm_give
    template_name = 'assets/assets-add-update-give.html'
    # success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):

        pk = self.request.path.split('.')[0].split('-')[-1]
        # print(pk)

        # print(reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,}))

        # print(self.request.path)
        b=self.request.path
        a=self.request.POST.copy()
        ret=re.search('-g-',b)

        user = self.request.POST['user']
        if assets.objects.get(uid=pk).active_id==1:
            if ret is None:
                a['active'] = 3
                self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'o','user':user})
            else:
                a['active'] = 2
                self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'l','user':user})
            # print(a)
            self.request.POST = a
        else :
            return HttpResponse('请先归还资产')

        return super().post(request, *args, **kwargs)


class AssetsUpdatein(LoginRequiredMixin,UpdateView):
    '''归还资产和资产报废'''
    model = assets
    form_class = AssetsForm_in
    template_name = 'assets/assets-add-update-in.html'
    # success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):
        b=self.request.path
        pk = self.request.path.split('.')[0].split('-')[-1]
        a=self.request.POST.copy()
        ret=re.search('-i-',b)
        if ret :
            a['active']=1
            a['user']=''
            a['otime']=''
            self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'i','user':'c'})

        else:
            a['active']=5
            a['user']=''
            a['otime']=''
            self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'p','user':'c'})


        self.request.POST=a
        return super().post(request, *args, **kwargs)



def repair(request,**kwargs):
    '''维修资产'''
    if request.method == 'GET':
        return render(request,'assets/wx_log.html')

    if request.method == 'POST':

        pk = request.path.split('.')[0].split('-')[-1]
        str_id = request.POST['wx']

        if assets.objects.get(uid=pk).active_id==1:

            assets.objects.filter(uid=pk).update(active_id=4)

        else :
            return HttpResponse('请先归还资产')
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'报修'+'  报修原因：'+str_id
        try:
            tb_log.objects.create(uid_id=pk,log_info=str1)
        except BaseException :
                return HttpResponse('数据录入成功，操作日志录入失败，请联系开发人员')
        else:
            return HttpResponseRedirect(reverse_lazy('assets:assets_list'))


def AssetsZtree(request):
    """
    获取 区域 资产树 的相关数据
    :param request:
    :return:
    """

    manager = active.objects.values()
    data = [{"id": "1111", "pId": "0", "name": "状态"}, ]
    for i in manager:
        # print(i['id'])
        data.append({"id": i['id'], "pId": "1111", "name": i['name'], "page": "xx.action"}, )
    return HttpResponse(json.dumps(data), content_type='application/json')




def excel_export(request):
    '''文件导出'''
    import xlwt
    from io import BytesIO

    if request.method == 'GET':
        list_obj = assets.objects.all().order_by('utype_id','active_id')
        style = xlwt.XFStyle()
        style.num_format_str='M/D/YY'
        if list_obj:
            fields = [field for field in assets._meta.fields]
            print(fields)

            header = [field.verbose_name for field in fields]
            ws = xlwt.Workbook(encoding='utf-8')
            w = ws.add_sheet(u'第一页数据')
            w.write(0, 0, header[0])
            w.write(0, 1, header[1])
            w.write(0, 2, header[2])
            w.write(0, 3, header[3])
            w.write(0, 4, header[4])
            w.write(0, 5, header[5])
            w.write(0, 6, header[6])
            w.write(0, 7, header[7])
            w.write(0, 8, header[8])
            w.write(0, 9, header[9])
            w.write(0, 10, header[10])
            w.write(0, 11, header[11])
            w.write(0, 12, header[12])
            w.write(0, 13, header[13])
            w.write(0, 14, header[14])


        excel_row = 1
        for obj in list_obj:
            w.write(excel_row,0,obj.uid)
            w.write(excel_row,1,obj.utype.name)
            w.write(excel_row,2,obj.usize.name)
            w.write(excel_row,3,obj.uconf)
            w.write(excel_row, 4, obj.active.name)
            w.write(excel_row, 5, obj.ctime, style)
            w.write(excel_row,6,obj.user)
            w.write(excel_row,7,obj.gtime,style)
            w.write(excel_row,8,obj.otime,style)
            w.write(excel_row, 9, obj.sn)
            w.write(excel_row, 10, obj.addr)
            w.write(excel_row, 11, obj.pid)
            w.write(excel_row, 12, obj.nmac)
            w.write(excel_row, 13, obj.wmac)
            w.write(excel_row, 14, obj.ps)

            excel_row +=1

        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        # print(response)
        # print(sio.getvalue())
        response['Content-Disposition'] = 'attachment; filename=test.xls'
        response.write(sio.getvalue())
        return response


    if request.method == 'POST':
        ids = request.POST.getlist('id', None)

        idstring = ''
        #####################################
        # '''使用weherw时字符串必须采用引号'''
        if ids:
            for i in ids:
                if i.isdigit():
                    idstring = idstring + str(i)+','
                else:
                    idstring = idstring+'\''+ str(i) +'\''+','
        idstring_new=idstring[0:-2]
        #######################################
        # idstring = ','.join(ids)
        qs = assets.objects.extra(where=['uid IN (' + idstring_new + ')']).all().order_by('utype_id','active_id')
        # print(qs)
        # print('uid IN (' + idstring + ')')
        style = xlwt.XFStyle()
        style.num_format_str='M/D/YY'

        ws = xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet(u'第一页数据')
        fields = [field for field in assets._meta.fields]
        # print(fields)

        header = [field.verbose_name for field in fields]
        # print(header)
        w.write(0, 0, header[0])
        w.write(0, 1, header[1])
        w.write(0, 2, header[2])
        w.write(0, 3, header[3])
        w.write(0, 4, header[4])
        w.write(0, 5, header[5])
        w.write(0, 6, header[6])
        w.write(0, 7, header[7])
        w.write(0, 8, header[8])
        w.write(0, 9, header[9])
        w.write(0, 10, header[10])
        w.write(0, 11, header[11])
        w.write(0, 12, header[12])
        w.write(0, 13, header[13])
        w.write(0, 14, header[14])
        if qs:
            excel_row = 1
            for obj in qs:
                w.write(excel_row,0,obj.uid)
                w.write(excel_row,1,obj.utype.name)
                w.write(excel_row,2,obj.usize.name)
                w.write(excel_row,3,obj.uconf)
                w.write(excel_row, 4, obj.active.name)
                w.write(excel_row, 5, obj.ctime, style)
                w.write(excel_row,6,obj.user)
                w.write(excel_row,7,obj.gtime,style)
                w.write(excel_row,8,obj.otime,style)
                w.write(excel_row, 9, obj.sn)
                w.write(excel_row, 10, obj.addr)
                w.write(excel_row, 11, obj.pid)
                w.write(excel_row, 12, obj.nmac)
                w.write(excel_row, 13, obj.wmac)
                w.write(excel_row, 14, obj.ps)
                excel_row +=1

        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        # print(response)
        # print(sio.getvalue())
        response['Content-Disposition'] = 'attachment; filename=test.xls'
        response.write(sio.getvalue())
        return response


def AssetsImport(request):

    """
    资产导入    """
    import  xlrd
    from datetime import datetime
    from xlrd import xldate_as_tuple
    fields = [field for field in assets._meta.fields]
    # print(fields)

    # header = [field.verbose_name for field in fields]
    # print(header)
    created, updated, failed = [], [], []
    mapping_reverse = [field.name for field in fields]
    # print(mapping_reverse)

    # type_all = platform.objects.all()
    # type_dict = {}
    # size_dict = {}
    # for i in type_all:
    #     type_dict[i.name]=i.id
    #     size_id_all = platform_size.objects.filter(platform__id=i.id)
    #     size_dict[i.id]=dict(zip([x.name for x in size_id_all],[x.id for x in size_id_all]))
    # print(type_dict)
    # print(size_dict)

    form = FileForm()
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            wb = xlrd.open_workbook(encoding_override='utf-8', filename=None,
                                    file_contents=request.FILES['file'].read())
            table = wb.sheets()[0]
            row = table.nrows  # 数据的行数
            for i in range(1,row):
                col = table.row_values(i)
                if set(col) == {''}:
                    continue
                else:
                    try:
                        col[1] = platform.objects.get(name=col[1])
                        col[2] = platform_size.objects.get(name=col[2], platform=col[1])
                        col[4] = active.objects.get(name=col[4])
                        for y in range(len(col)):
                            if table.cell(i, y).ctype == 3:
                                date = datetime(*xldate_as_tuple(col[y], 0))
                                col[y] = date.strftime('%Y-%m-%d')
                            if table.cell(i, y).ctype == 0:
                                col[y] = None

                        assets_au = dict(zip(mapping_reverse, col))
                    except:
                        return HttpResponse('导入文件格式错误')
                    # print(assets_au)
                    if assets.objects.filter(uid=col[0]):
                        try:
                            assets.objects.filter(uid=col[0]).update(**assets_au)
                        except BaseException as e:
                            failed.append('%s: %s' % (col[0], str(e)))
                        updated.append('%s' % (col[0]))
                        str1 = str(col[0]) + '在' + time.strftime("%Y-%m-%d", time.localtime(time.time())) + '导入更新成功'
                        tb_log.objects.create(uid_id=col[0], log_info=str1)

                    else:
                        try:
                            assets.objects.create(**assets_au)
                        except BaseException:
                            failed.append('%s: %s' % (col[0], str(e)))

                        created.append('%s' % (col[0]))
                        str1 = str(col[0]) + '在' + time.strftime("%Y-%m-%d", time.localtime(time.time())) + '导入创建成功'
                        tb_log.objects.create(uid_id=col[0], log_info=str1)

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

            return render(request, 'assets/assets-import.html', {'form': form, "msg": data, "assets_class": 'active'})

    return render(request, 'assets/assets-import.html', {'form': form, "assets_class": 'active'})







    # if table.cell(i, 5).ctype==3:
    #     date = datetime(*xldate_as_tuple(col[5], 0))
    #     col[5] = date.strftime('%Y-%d-%m')
    #
    # if table.cell(i, 7).ctype==3:
    #     date = datetime(*xldate_as_tuple(col[7], 0))
    #     col[7] = date.strftime('%Y-%d-%m')
    #
    # if table.cell(i, 8).ctype==3:
    #     date = datetime(*xldate_as_tuple(col[8], 0))
    #     col[8] = date.strftime('%Y-%d-%m')














    # asset1 = assets.objects.filter(id=col[0])
    # if asset1:
    #     raise

    #         f = form.cleaned_data['file']
    #
    #         det_result = chardet.detect(f.read())
    #         print(det_result,codecs.BOM_UTF8.decode())
    #         f.seek(0)  # reset file seek index
    #
    #         file_data = f.read().decode(det_result['encoding']).strip(codecs.BOM_UTF8.decode())
    #
    #         csv_file = StringIO(file_data)
    #         reader = csv.reader(csv_file)
    #         csv_data = [row for row in reader]
    #
    #         fields = [
    #             field for field in cmdb._meta.fields
    #         ]
    #
    #         header_ = csv_data[0]
    #         mapping_reverse = {field.verbose_name: field.name for field in fields}
    #         attr = [mapping_reverse.get(n, None) for n in header_]
    #
    #         created, updated, failed = [], [], []
    #
    #
    #         for row in csv_data[1:]:
    #             if set(row) == {''}:
    #                 continue
    #             asset_dict = dict(zip(attr, row))
    #             asset_dict_id = dict(zip(attr, row))
    #             ids = asset_dict['id']
    #             id_ = asset_dict.pop('id', 0)
    #             asset1 = cmdb.objects.filter(id=ids)  ##判断ID 是否存在
    #
    #             if not asset1:
    #                 try:
    #                     if len(cmdb.objects.filter(hostname=asset_dict.get('hostname'))):
    #                         raise Exception(('already exists'))
    #                     cmdb.objects.create(**asset_dict_id)
    #                     created.append(asset_dict['hostname'])
    #                 except Exception as e:
    #                     failed.append('%s: %s' % (asset_dict['hostname'], str(e)))
    #
    #             else:
    #                 for k, v in asset_dict.items():
    #                     if v:
    #                         setattr(cmdb, k, v)
    #                 try:
    #                     cmdb.objects.filter(id=ids).update(**asset_dict)
    #                     updated.append(asset_dict['hostname'])
    #                 except Exception as e:
    #                     failed.append('%s: %s' % (asset_dict['hostname'], str(e)))
    #
    #         data = {
    #             'created': created,
    #             'created_info': 'Created {}'.format(len(created)),
    #             'updated': updated,
    #             'updated_info': 'Updated {}'.format(len(updated)),
    #             'failed': failed,
    #             'failed_info': 'Failed {}'.format(len(failed)),
    #             'valid': True,
    #             'msg': 'Created: {}. Updated: {}, Error: {}'.format(
    #                 len(created), len(updated), len(failed))
    #         }
    #
    #         return render(request, 'cmdb/cmdb-import.html', {'form': form,
    #                                                            "msg": data})
    #
    # return render(request, 'cmdb/cmdb-import.html', {'form': form })
    #
    #






    #

    # a=self.request.POST.copy()
    # a['active']=1
    # a['user']=''
    # a['otime']=''
    # print(a)
    # self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'i','user':'c'})
    # self.request.POST=a





