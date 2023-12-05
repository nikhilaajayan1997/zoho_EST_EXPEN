# @login_required(login_url='login')
# def edited_prod(request, id):
#     print(id)
#     user = request.user
#     c = customer.objects.all()
#     p = AddItem.objects.filter(user = request.user)
#     invoiceitem = invoice_item.objects.filter(inv_id=id)
#     invoic = invoice.objects.get(id=id)
#     cust = invoic.customer.placeofsupply
#     cust_id = invoic.customer.id
#     pay = payment_terms.objects.filter(user = request.user)
#     sales = Sales.objects.all()
#     purchase = Purchase.objects.all()
#     invpay = InvoicePayment.objects.filter(invoice_id=id)
#     ip = InvoicePayment.objects.filter(invoice__user=request.user)



#     invp = invpay[0] if invpay else None
#     banks = Bankcreation.objects.all()
#     unit = Unit.objects.all()
    
#     company = company_details.objects.get(user=request.user.id)
#     comp = company.state
    

#     if request.method == 'POST':
#         x = request.POST["hidden_state"]
#         y = request.POST["hidden_cus_place"]
#         print("Value of x:", x)
#         print("Value of y:", y)
#         u = request.user.id
#         u2 = User.objects.get(id=u)
#         c = request.POST['cx_name']
#         cus = customer.objects.get(id=c)

#         invoic.customer = cus
#         invoic.user = u2
#         invoic.terms = request.POST.get('term', "")
#         invoic.inv_date = request.POST.get('inv_date', "")
#         invoic.due_date = request.POST.get('due_date', "")
#         invoic.cxnote = request.POST.get('customer_note', "")
#         invoic.subtotal = request.POST.get('subtotal', "")
#         invoic.igst = request.POST.get('igst', "")
#         invoic.cgst = request.POST.get('cgst', "")
#         invoic.sgst = request.POST.get('sgst', "")
#         invoic.t_tax = request.POST.get('totaltax', "")
#         invoic.grandtotal = request.POST.get('t_total', "")
#         invoic.paid_amount = request.POST.get('paid_amount', "")
#         invoic.balance = request.POST.get('balance', "")
#         if invoic.estimate:
#             est_obj=Estimates.objects.get(id=invoic.estimate)
#             est_obj.balance=invoic.balance
#             est_obj.save()

#         old = invoic.file
#         new = request.FILES.get('file')
#         if old and not new:
#             invoic.file = old
#         else:
#             invoic.file = new

#         invoic.terms_condition = request.POST.get('ter_cond')

        
        

#         invoic.save()
        
#         if invp:
#             invp.payment_method = request.POST.get('payment_method', "")
#             if invp.payment_method == 'cash':
#                 pass
#             elif invp.payment_method == 'cheque':
#                 invp.cheque_number = request.POST.get('cheque_number', '')
#             elif invp.payment_method == 'upi':
#                 invp.upi_id = request.POST.get('upi_id', '')
#             else:
#                 invp.bank_id = request.POST.get('bank_name', "")

#             invp.save()

#         print("/////////////////////////////////////////////////////////")
        
#         if x == y:
#             invoiceitem.item = request.POST.getlist('item[]')
#             invoiceitem.hsn = request.POST.getlist('hsn[]')
#             invoiceitem.quantity = request.POST.getlist('quantity[]')
#             invoiceitem.rate = request.POST.getlist('rate[]')
#             invoiceitem.desc = request.POST.getlist('desc[]')
#             invoiceitem.tax = request.POST.getlist('tax[]')
#             invoiceitem.amount = request.POST.getlist('amount[]')
            
#             print("hai")
            
#         else:
#             invoiceitem.itemm = request.POST.getlist('itemm[]')
#             invoiceitem.hsnn = request.POST.getlist('hsnn[]')
#             invoiceitem.quantityy = request.POST.getlist('quantityy[]')
#             invoiceitem.ratee = request.POST.getlist('ratee[]')
#             invoiceitem.descc = request.POST.getlist('descc[]')
#             invoiceitem.taxx = request.POST.getlist('taxx[]')
#             invoiceitem.amountt = request.POST.getlist('amountt[]')
            
            
#         if x == y:
#             print("manage")
#             print("Length of invoiceitem.item: ", len(invoiceitem.item))
#             print("Length of invoiceitem.hsn: ", len(invoiceitem.hsn))
#             print("Length of invoiceitem.quantity: ", len(invoiceitem.quantity))
#             print("Length of invoiceitem.desc: ", len(invoiceitem.desc))
#             print("Length of invoiceitem.tax: ", len(invoiceitem.tax))
#             print("Length of invoiceitem.amount: ", len(invoiceitem.amount))
#             print("Length of invoiceitem.rate: ", len(invoiceitem.rate))
#             print("Value of x: ", x)
#             print("Value of y: ", y)
#             if len(invoiceitem.item) == len(invoiceitem.hsn) == len(invoiceitem.quantity) == len(invoiceitem.desc) == len(invoiceitem.tax) == len(invoiceitem.amount) == len(invoiceitem.rate):
#                 print("11")
#                 mapped = zip(invoiceitem.item, invoiceitem.hsn, invoiceitem.quantity, invoiceitem.desc, invoiceitem.tax, invoiceitem.amount, invoiceitem.rate)
#                 mapped = list(mapped)
#                 for element in mapped:
#                     created = invoice_item.objects.get_or_create(inv=invoic, product=element[0], hsn=element[1],
#                                                                  quantity=element[2], discount=element[3], tax=element[4],
#                                                                  total=element[5], rate=element[6])
#                     print("moveon")

#                 return redirect('invoice_overview', id)

#         else:
#             if len(invoiceitem.itemm) == len(invoiceitem.hsnn) == len(invoiceitem.quantityy) == len(invoiceitem.descc) == len(invoiceitem.taxx) == len(invoiceitem.amountt) == len(invoiceitem.ratee):
#                 mapped = zip(invoiceitem.itemm, invoiceitem.hsnn, invoiceitem.quantityy, invoiceitem.descc, invoiceitem.taxx, invoiceitem.amountt, invoiceitem.ratee)
#                 mapped = list(mapped)
#                 for element in mapped:
#                     print("Debug - Values before filter:", invoic, element[0], element[1])
#                     existing_items = invoice_item.objects.filter(
#                         inv=invoic,
#                         product=element[0],
#                         hsn=element[1],
#                         quantity=element[2],
#                             discount=element[3],
#                             tax=element[4],
#                             total=element[5],
#                             rate=element[6]
#                     )

#                     if not existing_items.exists():
#                         created = invoice_item.objects.create(
#                             inv=invoic,
#                             product=element[0],
#                             hsn=element[1],
#                             quantity=element[2],
#                             discount=element[3],
#                             tax=element[4],
#                             total=element[5],
#                             rate=element[6]
#                         )
#                         print("Debug - After create")




#                 return redirect('invoice_overview', id)

#     context = {
#         'user': user,
#         'c': c,
#         'p': p,
#         'inv': invoiceitem,
#         'i': invoic,
#         'pay': pay,
#         'sales': sales,
#         'purchase': purchase,
#         'units': unit,
#         'company': company,
#         'cust': cust,
#         'comp': comp,
#         'custo_id': cust_id,
#         'invpay': invpay,
#         'banks': banks,
#         'invp':invp,
#          'ip':ip,
    
#     }

#     return render(request, 'invoiceedit.html', context)