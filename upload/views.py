

# views.py
from django.shortcuts import render, redirect
from .tasks import process_uploaded_files
from .models import BookingData, RefundData

def upload_files(request):
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        year = request.POST.get('year')
        month = request.POST.get('month')
        booking_or_refund = request.POST.get('booking_or_refund')
        files = request.FILES.getlist('files')

        # Process each uploaded file
        for f in files:
            file_content = f.read()  # Read file content
            print(file_content)
            file_name = f.name
            process_uploaded_files.delay(file_content, file_name, bank_name, year, month, booking_or_refund)

        return redirect('success')  # Redirect to success page

    return render(request, 'upload.html')



def display_data(request):
    bank_name = request.GET.get('bank_name')
    year = request.GET.get('year')
    month = request.GET.get('month')
    booking_or_refund = request.GET.get('booking_or_refund')
    date = request.GET.get('date')
    # sale_total = request.GET.get('sale_total')
    # sale_amount = request.GET.get('sale_amount')
    
    # sale_total = models.IntegerField()  # Store the total number of entries
    # date = models.DateField()  # Store the date from "CREDITED ON"
    # sale_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store the "BOOKING AMOUNT"


    # Filter the data based on user selection
    data = []
    if booking_or_refund == 'booking':
        data = BookingData.objects.filter(
            bank_name=bank_name, 
            year=year, 
            month=month,
            date=date,
            # sale_total = sale_total,
            # sale_amount = sale_amount   
        )
    # elif booking_or_refund == 'refund':
    #     data = RefundData.objects.filter(
    #         bank_name=bank_name, 
    #         year=year, 
    #         month=month,
    #         date=date
    #     )
    
    else:
        pass

    return render(request, 'display_data.html', {'data': data})

def upload_success(request):
    return render(request, 'upload_success.html')