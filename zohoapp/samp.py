def newestimate(request):
    user = request.user
    company = company_details.objects.get(user=user)
    cmp1=company.id
    items = AddItem.objects.filter(user_id=user.id)
    customers = customer.objects.filter(user_id=user.id)
    unit=Unit.objects.all()
    sales=Sales.objects.all()
    purchase=Purchase.objects.all()
    payments = payment_terms.objects.filter(user=user)
    print("helloooooooooooooooooooooooooo")

    try:
        latest_bill = ExpenseE.objects.filter(company = cmp1).order_by('-reference').first()
        # latest_bill = Estimates.objects.filter(company = cmp1).values_list('reference',flat=True).last()
        print("haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii") 
        if latest_bill:
                print("ssssssssssssssssssssssssssssssssssssssss") 
                last_number = int(latest_bill.reference)
                print(last_number)
                new_number = last_number + 1
                print(new_number)
        else:
                new_number = 1
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") 
        if deletedestimates.objects.filter(cid = cmp1).exists():
                deleted = deletedestimates.objects.get(cid = cmp1)
                if deleted:
                    while int(deleted.reference_number) >= new_number:
                        new_number+=1
        print("helloooooooooooooooooooooooooo")
        if Estimates.objects.filter(reference=1).exists():
                est_obj=Estimates.objects.get(reference=1)
                est_no=est_obj.estimate_no
                context = {'unit':unit,'company': company,'items': items,'customers': customers,'count':new_number,'sales':sales,'purchase':purchase,'payments':payments,'est_no':est_no}
                return render(request,'new_estimate.html',context)
        else:
                context = {'unit':unit,'company': company,'items': items,'customers': customers,'count':new_number,'sales':sales,'purchase':purchase,'payments':payments}
                return render(request,'new_estimate.html',context)
        
    
    except Exception as e:
        return redirect("allestimates")
                    
                    