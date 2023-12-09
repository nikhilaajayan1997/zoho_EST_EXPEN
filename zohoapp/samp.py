def shareSalesOrderToEmail(request,pk):
    if request.user: 
        try:
            if request.method == 'POST':
                emails_string = request.POST['email_ids']

                # Split the string by commas and remove any leading or trailing whitespace
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']
                # print(emails_list)

                cmp = company_details.objects.get( user = request.user.id)
                bill = Estimates.objects.get(id = pk)
                items = sales_item.objects.filter( sale = bill.id)
                        
                context = {'bill': bill, 'cmp': cmp,'items':items}
                template_path = 'sales_bill_pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                
                filename = f'Sales Bill - {bill.sales_no}.pdf'
                subject = f"SALES BILL - {bill.sales_no}"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached SALES BILL - Bill-{bill.sales_no}. \n{email_message}\n\n--\nRegards,\n{cmp.company_name}\n{cmp.address}\n{cmp.state} - {cmp.country}\n{cmp.contact_number}", from_email=settings.EMAIL_HOST_USER,to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                msg = messages.success(request, 'Bill has been shared via email successfully..!')
                return redirect(sales_order_det,id)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(sales_order_det, id)