def import_estimate(request):
    user1=request.user.id
    user2=User.objects.get(id=user1)
    cmp=company_details.objects.get(user=user1)
    if request.method == 'POST' and 'excel_file' in request.FILES:
        excel_file = request.FILES.get('excel_file')
        
        wb = load_workbook(excel_file)
        try:
            ws = wb["Sheet1"]
            header_row = ws[1]
            column_names = [cell.value for cell in header_row]
            print("Column Names:", column_names)
        except:
          print('sheet not found')
          messages.error(request,'`challan` sheet not found.! Please check.')
          return redirect('allestimates')
        
        ws = wb["Sheet1"]
        estimate_columns = ['SLNO','CUSTOMER NAME','CUSTOMER MAILID','ESTIMATE DATE','EXPIRY DATE','PLACE OF SUPPLY','SUB TOTAL','IGST','CGST','SGST','TAX AMOUNT','SHIPPING CHARGE','ADJUSTMENT','GRAND TOTAL','STATUS']
        estimate_sheet = [cell.value for cell in ws[1]]
        if estimate_sheet != estimate_columns:
          print('invalid sheet')
          messages.error(request,'`challan` sheet column names or order is not in the required formate.! Please check.')
          return redirect("allestimates")
        
        for row in ws.iter_rows(min_row=2, values_only=True):
          slno,customer_name,customer_mailid,estimate_date,expiry_date,place_of_supply,subtotal,igst,cgst,sgst,taxamount,shipping_charge,adjustment,grandtotal,status = row
          if slno is None or place_of_supply is None or taxamount is None or grandtotal is None:
            print('challan == invalid data')
            messages.error(request,'`challan` sheet entries missing required fields.! Please check.')
            return redirect("allestimates")
          
        # checking items sheet columns
        ws = wb["Sheet2"]
        items_columns = ['ESTIMATE NO','ITEM NAME','HSN','QUANTITY','RATE','TAX PERCENTAGE','DISCOUNT','AMOUNT']
        items_sheet = [cell.value for cell in ws[1]]
        if items_sheet != items_columns:
          print('invalid sheet')
          messages.error(request,'`items` sheet column names or order is not in the required formate.! Please check.')
          return redirect("allestimates")
        
        for row in ws.iter_rows(min_row=2, values_only=True):
          chl_no,item_name,hsn,quantity,rate,tax_percentage,discount,amount=row
          if chl_no is None or item_name is None or quantity is None or tax_percentage is None or amount is None:
            print('items == invalid data')
            messages.error(request,'`items` sheet entries missing required fields.! Please check.')
            return redirect("allestimates")
        
         # getting data from estimate sheet and create estimate.
        ws = wb['Sheet1']
        for row in ws.iter_rows(min_row=2, values_only=True):
            slno,customer_name,customer_mailid,estimate_date,expiry_date,place_of_supply,subtotal,igst,cgst,sgst,taxamount,shipping_charge,adjustment,grandtotal,status = row
            dcNo = slno
            if slno is None:
                continue
            # Fetching last bill and assigning upcoming bill no as current + 1
            # Also check for if any bill is deleted and bill no is continuos w r t the deleted bill
            latest_bill = Estimates.objects.filter(company = cmp).order_by('-reference').first()
            if latest_bill:
                last_number = int(latest_bill.reference)
                new_number = last_number + 1
            else:
                new_number = 1
            if deletedestimates.objects.filter(cid = cmp).exists():
                    deleted = deletedestimates.objects.get(cid = cmp)
                    if deleted:
                        while int(deleted.reference_number) >= new_number:
                            new_number+=1
            if Estimates.objects.filter(company=cmp,reference=1).exists():
                estobj=Estimates.objects.get(company=cmp,reference=1)
                estno=estobj.estimate_no
                refno=estobj.reference
                print("eeeeeeeeee   ssssssssssssssss   tttttttttttttttttttt")
                ref_len=len(str(refno))
                ref_len2=int(ref_len)
                
                sliced_str=estno[:-ref_len2]
                print("eeeeeeeeee   ssssssssssssssss   tttttttttttttttttttt")
                print(sliced_str)
                print("-------------------------------------------------------------")
                estno=sliced_str+str(new_number)
            else:
                estno="EST-"+str(new_number)
            custname=customer_name.upper()
            cust=customer.objects.get(customerEmail=customer_mailid)
            challn=Estimates(customer_name=custname,customer_mailid=customer_mailid,customer_placesupply=place_of_supply,
                            reference=new_number,estimate_date=estimate_date,expiry_date=expiry_date,sub_total=subtotal,igst=igst,
                            cgst=cgst,sgst=sgst,tax_amount=taxamount,shipping_charge=shipping_charge,adjustment=adjustment,total=grandtotal,
                            status=status,estimate_no=estno,convert_invoice='not_converted',convert_sales='not_converted',
                            convert_recinvoice='not_converted',company=cmp,customer=cust,user=user2)
            challn.save()
            # Items for the estimate
            ws = wb['Sheet2']
            for row in ws.iter_rows(min_row=2, values_only=True):
                chl_no,item_name,hsn,quantity,rate,tax_percentage,discount,amount=row
                if int(chl_no) == int(dcNo):
                    print(row)
                if discount is None:
                    discount=0
                # if price is None:
                #     price=0
                EstimateItems.objects.create(item_name = item_name,hsn=hsn,quantity=int(quantity),rate = float(rate),tax_percentage=tax_percentage,discount = float(discount),amount=amount,estimate=challn)
        messages.success(request, 'Data imported successfully.!')
        return redirect("allestimates")
           