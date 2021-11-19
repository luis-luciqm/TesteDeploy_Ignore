from django.http import Http404,JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView,ListView,UpdateView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from .models import *
from management.models import *
from .forms import ProductForm,CategoriaForm,CaptureForm, CommentForm

from sweetify.views import SweetifySuccessMixin
from utils.Sweetify_Styles import Sweetify_Styles

from django.core.paginator import Paginator
from django.contrib import messages

from django.db.models import Count
from django.conf import settings
import time

import requests
import webbrowser
from rolepermissions.mixins import HasRoleMixin


#qtd de anuncios por paginas
ITEM_PAGES = 10


# Create your views here.
class ProductCreateView(HasRoleMixin,SweetifySuccessMixin,CreateView):
    model = Product
    #template_name = 'product/teste_categoria.html'
    template_name = 'product/form_create_product.html'
    allowed_roles = 'administrador'

    form_class = ProductForm
    success_url = '/gerenciamento/'
    
    success_message = 'Produto Cadastrado com sucesso!'
    sweetify_options = Sweetify_Styles.styles_sucess()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorys'] = list(Category.objects.order_by("name").all())
        context['subcategorys'] = list(SubCategory.objects.order_by("name").all())
        return context
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        ad = self.object = form.save(commit=False)
        # self.object.short_url = link_retorno
        # self.object.long_url = link_retorno
        ad.user = self.request.user
        return super().form_valid(form)
    
    def get_initial(self):
        super(ProductCreateView,self).get_initial()
        long_url = self.request.session.get('site_url', False)
        short_url = ''
        if long_url:  
            short_url = generate_link_curto(long_url)
        self.initial = {"long_url": long_url, "short_url": short_url,}
        return self.initial

def generate_link_curto(long_url):
        data =  {	
            "long_url": f"{long_url}"  
        }  
        url = 'https://api-ssl.bitly.com/v4/shorten'

        head = {    
                    "Authorization": "Bearer 0d993a38764443ddaed000c43384a9d103f4b828"
                }

        response = requests.post(url=url, json=data, headers= head)
        return response.json()['link']



def generate_linK_id_parceiro(url):
    stores = Store.objects.all()
    LINK_RETORNO = ''
    
    if 'magazineluiza.com' in url: # permiti fazer links de magazine luiza
        s = Store.objects.get(name__icontains='Magazine')
        id_link_product = url.split('https://www.magazineluiza.com.br/')
        retira_variaveis = id_link_product[1].split('?')
        link_store = s.url.rstrip('/')
        LINK_RETORNO = link_store+'/'+s.id_partner+'/'+retira_variaveis[0]
    elif 'magazinevoce.com' in url: #permite fazer links de magazinevoce
        s = Store.objects.get(name__icontains='Magazine')
        id_link_product = url.split('https://www.magazinevoce.com.br/')
        retira_variaveis = id_link_product[1].split('?')
        link_store = s.url.rstrip('/')
        aux = retira_variaveis[0].split('/')
        aux.pop(0) 
        product =''
        for p in aux:
            product += (p +'/')
        
        LINK_RETORNO = link_store+'/'+s.id_partner+'/'+product.rstrip('/')
    elif 'amazon.com' in url:
        # parametros que podem vim com o link da amazon | th e psc são de tamanho, k e rh são de busca
        th=""   
        psc ="" 
        k = ""
        rh = ""
        s = Store.objects.get(name__icontains='amazon') # pega a amazon no banci
        if s:
            if not 'https://' in s.url: #verifica se exite htpps no link da loja, para não gera erros
                url_aux = 'https://'+s.url
            else:
                url_aux = s.url
                
            id_link_product = url.split(url_aux)
            aux = id_link_product[1].split('?') # retirando todas as variaveis
            if len(aux) > 1:
                if 'th=' in aux[1] or 'psc=' in aux[1] or 'k=' in aux[1] or 'rh=' in aux[1]: # verificando se existe as variaveis de tamanho e busca
                    for parametros in aux[1].split('&'):
                        if 'th=' in parametros:
                            th = parametros
                        if 'psc=' in parametros:
                            psc = parametros
                        if 'k=' in parametros:
                            k = parametros
                            # print('oi')
                        if 'rh=' in parametros:
                            rh = parametros
            link_store = url_aux.rstrip('/') # caso o link da loja tenha sido salvo com uma / no fim ele retira
            LINK_RETORNO = link_store+'/'+aux[0].rstrip('/')+'/'+s.id_partner
            if th != "": # concatenando as variaveis de tamanho
                LINK_RETORNO = LINK_RETORNO +'&'+th
            if psc != "":
                LINK_RETORNO = LINK_RETORNO +'&'+psc  
            if k != "":
                LINK_RETORNO = LINK_RETORNO +'&'+k 
            if rh != "":
                LINK_RETORNO = LINK_RETORNO +'&'+rh
        
        # print(LINK_RETORNO)
    elif 'zattini.com' in url:
        s = Store.objects.get(name__icontains='zattini')
        campaign=""
        if s:
            if not 'https://' in s.url:
                url_aux = 'https://'+s.url
            else:
                url_aux = s.url
            id_link_product = url.split(url_aux)
            aux = id_link_product[1].split('?') # retirando todas as variaveis
            if len(aux) > 1:
                if 'campaign=' in aux[1]: # verificando se existe as variaveis de tamanho
                    for x in aux[1].split('&'):
                        if 'campaign=' in x:
                            campaign = x
                
                link_store = url_aux.rstrip('/')
                LINK_RETORNO = s.id_partner+link_store+'/'+aux[0]
                if campaign != "": # concatenando as variaveis de tamanho
                    LINK_RETORNO = LINK_RETORNO +'?'+campaign
            else:
                link_store = url_aux.rstrip('/')
                LINK_RETORNO = s.id_partner+link_store+'/'+aux[0]
                if campaign != "": # concatenando as variaveis de tamanho
                    LINK_RETORNO = LINK_RETORNO +'?'+campaign
    else: # fazendo link para qualquer outra loja
        for store in stores:
            try: 
                if store.url in url: # VERIFICANDO DE QUAL LOJA É O LINK
                    if not 'https://' in store.url:
                        url_aux = 'https://'+store.url
                        id_link_product = url.split(url_aux)
                        aux = id_link_product[1].split('?') # retirando todas as variaveis
                        link_store = url_aux.rstrip('/')
                    else:
                        id_link_product = url.split(store.url) # pegando apenas o produto
                        aux = id_link_product[1].split('?') # retirando todas as variaveis
                        link_store = store.url.rstrip('/') # caso tenha salvo a url sa loja com / no fim é retirado aqui
                    if store.style_link == 'I': # VERIFICANDO EM QUAL POSIÇÃO ESTÁ O ID DO PARCEIRO
                        LINK_RETORNO = store.id_partner+link_store+'/'+aux[0]
                    elif store.style_link == 'M':
                        LINK_RETORNO = link_store+'/'+store.id_partner+'/'+aux[0]
                    else:
                        LINK_RETORNO = link_store+'/'+aux[0]+'/'+store.id_partner
            except:
                pass
        # print(LINK_RETORNO)   
    return LINK_RETORNO

#TELA DE DETALHES
class ProductDetailView(LoginRequiredMixin,DetailView):
    model = Product
    form_class = CommentForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Product.objects.get(pk = self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(product = self.kwargs['pk'], active= True).order_by('-created')
        context['reports'] = Report_Problem.objects.filter(product = self.kwargs['pk'])
        context['number_report'] = Report_Problem.objects.filter(product = self.kwargs['pk']).count()
        return context
    
def addAnswerComment(request, pk):
    form = CommentForm(request.POST or None) # Recenbendo os dados do campo
    comment = Comment.objects.get(pk = pk) # pegando qual comentario vai adicionar resposta
    new = Comment(text = form['text'].value(), product = comment.product, author = request.user, parent = None, active = False) #criando o novo objeto para adicionar no parent
    new.save()
    # print("\n\n\n\n\n{}\n\n\n\n".format(request.META['HTTP_HOST']))
    comment.parent = new #salvando o objeto no parente do comentario
    comment.save()
    return redirect ('detalhes_produto', comment.product.pk)

#TELA DE LISTAR ANUNCIOS
class ProductListView(HasRoleMixin,LoginRequiredMixin,ListView):
    model = Product
    template_name = "product/list_products_teste.html"
    paginate_by = ITEM_PAGES
    allowed_roles = 'administrador'

    def get_queryset(self):
        products=''
        try:
            if self.kwargs['option'].lower() == 'ativos':
                products = Product.objects.filter(status='ACTIVE').order_by()
                
            elif self.kwargs['option'].lower() == 'pendentes':
                products = Product.objects.filter(status='PENDING')
            
            elif self.kwargs['option'].lower() == 'encerrados':
                products = Product.objects.filter(status='CLOSED')

            elif self.kwargs['option'].lower() == 'destacados':
                products = Product.objects.filter(relevant=True)

            elif self.kwargs['option'].lower() == 'exclusivos':
                products = Product.objects.filter(exclusive=True)

            elif self.kwargs['option'].lower() == 'reportados':
                products = Product.objects.raw('select * from product_product where id in (select product_id from product_report_problem where checked = false group by product_id)')
            else:
                products = Product.objects.all()
                     
        except Exception as e:
            # print('erro ', e)
            pass
            
        if self.kwargs['option'].lower() == 'reportados':
            object_list = products
        else:
             object_list = products.order_by('-created_at')
             
        if self.request.GET.get('search'):
            title = self.request.GET.get('search')
            object_list = object_list.filter(title__icontains=title)
                
        if self.request.GET.get('search_category'):
            subcategory = self.request.GET.get('search_category')
            object_list = object_list.filter(subcategory__name = subcategory)
        
        return object_list
    
    def get_context_data(self, **kwargs):
        # products = Product.objects.all()
        context = super().get_context_data(**kwargs)
        if self.kwargs['option'].lower() == 'ativos':
            context['color_navbar_active'] = 'active'
        elif self.kwargs['option'].lower() == 'pendentes':
            context['color_navbar_pending'] = 'active'
        elif self.kwargs['option'].lower() == 'encerrados':
            context['color_navbar_closed'] = 'active'
        elif self.kwargs['option'].lower() == 'destacados':
            context['color_navbar_relevant'] = 'active'
        elif self.kwargs['option'].lower() == 'exclusivos':
            context['color_navbar_exclusive'] = 'active'
        elif self.kwargs['option'].lower() == 'reportados':
            context['color_navbar_reports'] = 'active'
        else:
            context['color_navbar_all'] = 'active'
                
        context['all_products'] = Product.objects.all().count()
        context['products_active'] = Product.objects.filter(status='ACTIVE').count()
        context['products_pending'] = Product.objects.filter(status='PENDING').count()
        context['products_closed'] = Product.objects.filter(status='CLOSED').count()
        context['products_highlight'] = Product.objects.filter(relevant = True).count()
        context['all_subcategorys'] = SubCategory.objects.all()
        context['products_exclusive'] = Product.objects.filter(exclusive = True).count()
        context['products_reports'] = Report_Problem.objects.filter(checked = False).values('product').annotate(dcount = Count('product')).count()
        return context
        
class ProductUpdateView(HasRoleMixin,SweetifySuccessMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name='product/form_create_product.html'
    allowed_roles = 'administrador'

    success_message = 'Produto Alterado com sucesso!'
    sweetify_options = Sweetify_Styles.styles_sucess()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorys'] = list(Category.objects.all())
        context['subcategorys'] = list(SubCategory.objects.all())
        context['domain_url'] = settings.DOMAIN_URL
        return context
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        ad = self.object = form.save(commit=False)
        # self.object.short_url = link_retorno
        # self.object.long_url = link_retorno
        if self.kwargs['option'].lower() == 'publicar':
            ad.status = 'ACTIVE'
            ad.user = self.request.user
            push_notification(ad)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):    
        if self.kwargs['option'].lower() == 'atualizar': 
            return reverse_lazy('editar_produto', kwargs = {'pk':self.kwargs['pk'], 'option': 'atualizar'})
        
        product = Product.objects.get(pk = self.kwargs['pk'])
        webbrowser.open(f'{settings.DOMAIN_URL}/oferta/{product.slug}', new=2)  
        return reverse_lazy('editar_produto', kwargs = {'pk': self.kwargs['pk'], 'option':'atualizar'}) 
        # print(self.kwargs['pk'],'\n')

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "product/product_detail.html"

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug = slug, active = True)
        try:
            instance = Product.objects.get(slug = slug, active = True)
        except Product.DoesNotExist:
            raise Http404("Não encontrado!")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug = slug, active = True)
            instance =  qs.first()
        return instance

#TELA DE ANUNCIOS DESTACADOS  
class ActionProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = "product/list_products_teste.html"
    context_object_name = 'products'
    paginate_by = ITEM_PAGES

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['color_navbar_pending'] = 'active'
        context['all_products'] = Product.objects.all().count()
        context['products_active'] = Product.objects.filter(status='ACTIVE').count()
        context['products_inactive'] = Product.objects.filter(status='INACTIVE').count()
        context['products_pending'] = Product.objects.filter(status='PENDING').count()
        context['products_closed'] = Product.objects.filter(status='CLOSED').count()
        context['products_highlight'] = Product.objects.filter(relevant = True).count()
        context['products_exclusive'] = Product.objects.filter(exclusive = True).count()
        context['all_subcategorys'] = SubCategory.objects.all()
        context['products_reports'] = Report_Problem.objects.filter(checked = False).values('product').annotate(dcount = Count('product')).count()
        return context
    
    def get_queryset(self):
            products = Product.objects.filter(exclusive = True).count()
            product = Product.objects.get(pk=self.kwargs['pk'])
            if self.kwargs['option'].lower() == 'ativar':
                product.status = 'ACTIVE'
            elif self.kwargs['option'].lower() == 'encerrar':
                if product.exclusive:
                    product.exclusive = False
                    product.relevant = True
                    product.status = "CLOSED"
                else:
                    product.status = "CLOSED"
                    if product.relevant:
                        product.relevant = False
            elif self.kwargs['option'].lower() == 'add_destaques':
                product.relevant = True
            elif self.kwargs['option'].lower() == 'remove_destaques':
                product.relevant = False
            elif self.kwargs['option'].lower() == 'add_exclusivos':
                if products >= 6:
                    messages.error(self.request,'Já existem 6 produtos exclusivos, para prosseguir remova algum deles')
                else:
                    product.exclusive = True
            elif self.kwargs['option'].lower() == 'remove_exclusivos':
                product.exclusive = False
            
              
            product.save()
            object_list = Product.objects.filter(status='PENDING')
            return object_list 
        
class hightlightListView(HasRoleMixin,LoginRequiredMixin,ListView):
    model = Product
    template_name = "product/hightlight_product.html"
    queryset = Product.objects.filter(relevant = True)
    context_object_name = "products"
    allowed_roles = 'administrador'
    
    def get_queryset(self):
        title = self.request.GET.get('search')
        object_list = Product.objects.filter(relevant = True)
        if title:
            object_list = object_list.filter(title__icontains=title)
        return object_list
    
class RemoveHighlightsView(LoginRequiredMixin, ListView): 
    model = Product
    template_name = "product/hightlight_product.html"
    queryset = Product.objects.filter(relevant = True)
    
    def get_queryset(self):
        if self.kwargs['pk']:
            product = Product.objects.get(pk=self.kwargs['pk'])
            product.relevant = False
            product.save()
        title = self.request.GET.get('search')
        object_list = Product.objects.filter(relevant = True)
        if title:
            object_list = object_list.filter(title__icontains=title)
        return object_list
    
# ANUNCIOS NÂO ENVIADOS ++++++++++++++++++++++++++++++++++++++++++
class PendenciesListView(ListView):
    model = Product
    template_name = "product/pendencies_product.html"
    context_object_name = "products"
    paginate_by = ITEM_PAGES
    
    def get_queryset(self):
        title = self.request.GET.get('search')
        object_list = Product.objects.all()
        if title:
            object_list = object_list.filter(title__icontains=title)
        return object_list

class ActiveProductListView2(LoginRequiredMixin,ListView):
    model = Product
    template_name = "product/pendencies_product.html"
    queryset = Product.objects.filter(active=True)
    context_object_name = "products"
    paginate_by = ITEM_PAGES
            
class HighlightProductListView2(LoginRequiredMixin,ListView):
    model = Product
    template_name = "product/pendencies_product.html"
    queryset = Product.objects.filter(relevant = True)
    context_object_name = "products"
    paginate_by = ITEM_PAGES

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#comments
def DesactivateComment(self, id_comment, pk):
    comment = Comment.objects.get(pk = id_comment)
    comment.active = False
    comment.save()
    
    return redirect('detalhes_produto', pk)
    
        
#Revisar
class ProductCommentListView(HasRoleMixin, ListView):
    model = Comment
    template_name = 'product/product_comment.html'
    context_object_name = "comments"
    paginate_by = ITEM_PAGES
    allowed_roles = 'administrador'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain_url'] = settings.DOMAIN_URL
        return context
    
    def get_queryset(self, **kwargs):
        comments = Comment.objects.filter(active=True).order_by('-created')
        return comments

#Revisar
class ProductReportListView(HasRoleMixin,LoginRequiredMixin,ListView):
    model = Product
    template_name = "product/product_report.html"
    context_object_name = "products"
    allowed_roles = 'administrador'

    def get_queryset(self):
        object_list = Product.objects.raw('select * from product_product where id in (select product_id from product_report_problem where checked = false group by product_id)')
        return object_list

#Revisar
class CheckedReportView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/product_report.html"
    context_object_name = "products"
    
    def get_queryset(self):
        # print(self.kwargs['pk'],'\n\n')
        report = Report_Problem.objects.filter(product_id=self.kwargs['pk'])
        for aux in report: 
            aux.checked = True
            aux.save()
        
        products = Product.objects.all()
        reports = Report_Problem.objects.filter(checked = False)
        object_list = []
        aux = []
        
        for product in products:
            if reports.filter(product = product):
                aux.append(product) 
                
        object_list = aux
        return object_list

#Revisar
class AllCheckedReportView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/product_report.html"
    context_object_name = "products"
    
    def get_queryset(self):
        reports = Report_Problem.objects.all()
        
        for report in reports:
            report.checked = True
            report.save()
            
        object_list = ''
        return object_list
        
class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/produto/listar_produto/pendentes/'


def gerar_link_ajax(request):
    data=[]
    url_process = ""
    if request.method == "POST":
             
        try:
            url_process = request.POST['data_url'] 
            url_process = generate_linK_id_parceiro(url_process)
            url_short = generate_link_curto(url_process)

        except Exception as e: 
            # print(e)
            return JsonResponse(data, safe=False)
    
    return JsonResponse({'url_long': url_process, 'url_short': url_short }, safe = False)

    
class DestroyAllProductsPending(LoginRequiredMixin, ListView):
    model = Product
    template_name = "product/list_products_teste.html"
    context_object_name = "products"
    
    def get_queryset(self):
        products = Product.objects.filter(status="PENDING")
        products.delete()
        return []  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['color_navbar_pending'] = 'active'
        context['all_products'] = Product.objects.all().count()
        context['products_active'] = Product.objects.filter(status='ACTIVE').count()
        context['products_inactive'] = Product.objects.filter(status='INACTIVE').count()
        context['products_pending'] = Product.objects.filter(status='PENDING').count()
        context['products_closed'] = Product.objects.filter(status='CLOSED').count()
        context['products_highlight'] = Product.objects.filter(relevant = True).count()
        context['products_exclusive'] = Product.objects.filter(exclusive = True).count()
        context['all_subcategorys'] = SubCategory.objects.all()
        context['products_reports'] = Report_Problem.objects.filter(checked = False).values('product').annotate(dcount = Count('product')).count()
        return context

    
def productOpenAllReports(request):
    object_list = Product.objects.raw('select * from product_product where id in (select product_id from product_report_problem where checked = false group by product_id)')

    for product in object_list:
        url = settings.DOMAIN_URL + '/oferta/' + product.slug
        time.sleep(1)
        webbrowser.open(url, new=0)

    return redirect('anuncios_reportados')
    
    
def push_notification(produto):
    title = "Nova Pechincha na sua lista de desejos"
    body = produto.title
    a_remover = ['de', 'para', 'as', 'pelo', 'site', 'compre', 'com', 'em', 'ml', 'por', 'do', 'da', 'l', '-', '/','?',')','(',',','°']
    palavras = produto.title
    for x in a_remover:
        palavras = palavras.replace(x,"")
    
    palavras = palavras.split(' ')
    
    # palavras = ['tiringa','teste','teste01','teste02','teste03','teste04']
    for index, palavra in enumerate(palavras[:5]):
        condicao = "\'"+palavra+"' in topics"
        for i in range(index + 1,len(palavras)):
            condicao += " && !('"+palavras[i]+"' in topics)"
        data = { 
            "condition":condicao,
            "data": {
                "product":f"https://teste.pechinchou.com.br/oferta/{produto.slug}", ##revisar com nicodemos o link
                "click_action":"FLUTTER_NOTIFICATION_CLICK"
            },
            "notification":{
                "title":title,
                "body":body,
                "vibrate":1,
                "sound":1,
                "image":"https://admin.pechinchou.com.br/media/{produto.image}"
            },  
            "priority":"high",
            "click_action":"FLUTTER_NOTIFICATION_CLICK"
            
        }

        head = {    
            "Authorization": "Bearer AAAA5pqw4bI:APA91bFR9xappiU9TLlKOWlixfIhe-KgRsy01YetJy9U9oiGifDOWVnX9QA8u2A1NG5rK3Xc1AZt70WqUNEOP4i_XgKQsnitPdo-fb4Qm0Xj7g29BLyVpwyccv3cRv0rNnYTyfZr7gkk"
        }

        response = requests.post(json=data, url= 'https://fcm.googleapis.com/fcm/send', headers=head)

    return 'ok'
