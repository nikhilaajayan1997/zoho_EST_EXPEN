# def importChallanFromExcel(request):
#   if 'staff_id' in request.session:
#     if request.session.has_key('staff_id'):
#       staff_id = request.session['staff_id']
            
#     else:
#       return redirect('/')
#     staff =  staff_details.objects.get(id=staff_id)
#     com =  company.objects.get(id = staff.company.id)    
    
#     current_datetime = timezone.now()
#     dateToday =  current_datetime.date()

#     if request.method == "POST" and 'excel_file' in request.FILES:
    
#         excel_file = request.FILES['excel_file']

#         wb = load_workbook(excel_file)

#         # checking challan sheet columns
#         try:
#           ws = wb["challan"]
#         except:
#           print('sheet not found')
#           messages.error(request,'`challan` sheet not found.! Please check.')
#           return redirect(delivery_challan)

#         ws = wb["challan"]
#         estimate_columns = ['SLNO','DATE','DUE DATE','NAME','STATE OF SUPPLY','DESCRIPTION','SUB TOTAL','IGST','CGST','SGST','TAX AMOUNT','ADJUSTMENT','GRAND TOTAL']
#         estimate_sheet = [cell.value for cell in ws[1]]
#         if estimate_sheet != estimate_columns:
#           print('invalid sheet')
#           messages.error(request,'`challan` sheet column names or order is not in the required formate.! Please check.')
#           return redirect(delivery_challan)

#         for row in ws.iter_rows(min_row=2, values_only=True):
#           slno,date,due_date,name,state_of_supply,description,subtotal,igst,cgst,sgst,taxamount,adjustment,grandtotal = row
#           if slno is None or state_of_supply is None or taxamount is None or grandtotal is None:
#             print('challan == invalid data')
#             messages.error(request,'`challan` sheet entries missing required fields.! Please check.')
#             return redirect(delivery_challan)
        
#         # checking items sheet columns
#         ws = wb["items"]
#         items_columns = ['CHALLAN NO','NAME','HSN','QUANTITY','PRICE','TAX PERCENTAGE','DISCOUNT','TOTAL']
#         items_sheet = [cell.value for cell in ws[1]]
#         if items_sheet != items_columns:
#           print('invalid sheet')
#           messages.error(request,'`items` sheet column names or order is not in the required formate.! Please check.')
#           return redirect(delivery_challan)

#         for row in ws.iter_rows(min_row=2, values_only=True):
#           chl_no,name,hsn,quantity,price,tax_percentage,discount,total = row
#           if chl_no is None or name is None or quantity is None or tax_percentage is None or total is None:
#             print('items == invalid data')
#             messages.error(request,'`items` sheet entries missing required fields.! Please check.')
#             return redirect(delivery_challan)
        
#         # getting data from estimate sheet and create estimate.
#         ws = wb['challan']
#         for row in ws.iter_rows(min_row=2, values_only=True):
#           slno,date,due_date,name,state_of_supply,description,subtotal,igst,cgst,sgst,taxamount,adjustment,grandtotal = row
#           dcNo = slno
#           if slno is None:
#             continue
#           # Fetching last bill and assigning upcoming bill no as current + 1
#           # Also check for if any bill is deleted and bill no is continuos w r t the deleted bill
#           latest_bill = DeliveryChallan.objects.filter(company = com).order_by('-id').first()
          
#           if latest_bill:
#               last_number = int(latest_bill.challan_no)
#               new_number = last_number + 1
#           else:
#               new_number = 1

#           if DeletedDeliveryChallan.objects.filter(company = com).exists():
#               deleted = DeletedDeliveryChallan.objects.get(company = com)
              
#               if deleted:
#                   while int(deleted.challan_no) >= new_number:
#                       new_number+=1
#           try:
#             cntct = party.objects.get(company = com, party_name = name).contact
#             adrs = party.objects.get(company = com, party_name = name).address
#           except:
#             pass

#           if date is None:
#             date = dateToday

#           if due_date is None:
#             due_date = dateToday

#           print(date,due_date,new_number,name,cntct,adrs,state_of_supply,description,subtotal,igst,cgst,sgst,taxamount,adjustment,grandtotal)

#           challan = DeliveryChallan(
#               staff = staff,
#               company = com,
#               date = date,
#               due_date = due_date,
#               challan_no = new_number,
#               party_name = name,
#               contact = cntct,
#               billing_address = adrs,
#               state_of_supply = 'State' if str(state_of_supply).lower() == 'state' else 'Other State',
#               description = description,
#               subtotal = subtotal,
#               cgst = cgst,
#               sgst = sgst,
#               igst = igst,
#               tax_amount = taxamount,
#               adjustment = adjustment,
#               total_amount = grandtotal,
#               balance = 0,
#               status = 'Open',
#               is_converted = False
#           )
#           challan.save()

#           # Transaction history
#           history = DeliveryChallanTransactionHistory(
#             staff = staff,
#             challan = challan,
#             company = com,
#             action = "Create"
#           )
#           history.save()

#           # Items for the estimate
#           ws = wb['items']
#           for row in ws.iter_rows(min_row=2, values_only=True):
#             chl_no,name,hsn,quantity,price,tax_percentage,discount,total = row
#             if int(chl_no) == int(dcNo):
#               print(row)
#               if challan.state_of_supply == 'State' and tax_percentage:
#                 tx = 'GST'+str(tax_percentage)+'['+str(tax_percentage)+'%]'
#               elif challan.state_of_supply == 'Other State' and tax_percentage:
#                 tx = 'IGST'+str(tax_percentage)+'['+str(tax_percentage)+'%]'
#               if discount is None:
#                 discount=0
#               if price is None:
#                 price=0
#               try:
#                 itm = ItemModel.objects.get(company = com, item_name = name)
#               except:
#                 pass
#               DeliveryChallanItems.objects.create(staff = staff, cid = challan, company = com, item = itm,name = name,hsn=hsn,quantity=int(quantity),price = float(price),tax=tx, discount = float(discount),total=float(total))
#     messages.success(request, 'Data imported successfully.!')
#     return redirect(delivery_challan)