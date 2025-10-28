from django.db import connection
from django.shortcuts import render
from django.http import Http404


def dictfetchall(cursor):
    # Returns all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# Create your views here.
def index(request):
    return render(request, 'index.html')


def Query_answers(request):
    with connection.cursor() as cursor:
        # Execute Query 1
        cursor.execute("""  
            select distinct I.Name, round(Sum(B.BQuantity * S.Price),3) as total_Spent
            from Investor I, Buying B inner join diverse_investor DI on DI.ID = B.ID
            inner join Stock S on B.Symbol = S.Symbol and B.tDate = S.tDate
            where I.ID = B.ID
            group by I.Name
            order by total_Spent desc
        """)
        sql_res1 = dictfetchall(cursor)

        # Execute Query 2
        cursor.execute(""" 
            select TB.SYMBOL, TB.NAME, TB.QUANTITY
            FROM Top_buyers TB
            WHERE TB.Quantity = (
                select MAX(TB1.Quantity) AS MAX_QUANTITY
                FROM Top_buyers TB1
                WHERE TB.symbol = TB1.symbol
                group by TB1.symbol
            )
            ORDER BY Quantity DESC
        """)
        sql_res2 = dictfetchall(cursor)

        # Execute Query 3
        cursor.execute(""" 
                    select pc.symbol , count(distinct B.ID) as buyers_number
                    from profitable_company pc left outer join Buying B on b.Symbol=pc.symbol and b.tDate=pc.tdate
                    group by pc.symbol
                    order by buyers_number desc
                """)
        sql_res3 = dictfetchall(cursor)
    return render(request, 'Query_Answers.html', {'sql_res1': sql_res1, 'sql_res2': sql_res2, 'sql_res3': sql_res3})


def last_date(request):
    # this function finds the last day in stock database
    with connection.cursor() as cursor:
        cursor.execute(""" 
            select distinct max(tdate) as date
            from Stock
        """)
        sql_res = dictfetchall(cursor)
        if sql_res:
            return sql_res[0]['date']
        return None


def Add_transaction(request):
    with connection.cursor() as cursor:
        if request.POST:
            Id = request.POST["id"]
            amount = request.POST["transaction_sum"]
            last_transaction_date = last_date(request)

            # Check if the Investor exists
            cursor.execute("""
                            SELECT ID
                            FROM Investor
                            WHERE ID = %s;
                            """, [request.POST["id"]])
            sql_res4A = dictfetchall(cursor)

            if len(sql_res4A) == 0:
                raise Http404(f"Investor with ID {Id} does not exist.")

            cursor.execute("""
                            Select T.ID
                            from Transactions T
                            where T.tdate = %s
                            and T.ID = %s
                            """, [last_transaction_date, Id])
            sql_res4B = dictfetchall(cursor)
            if len(sql_res4B) != 0:
                raise Http404(f"Investor with ID {Id} already made a transaction in the date.")
            # If exists but not in transactions on last day

            cursor.execute("""
                            INSERT INTO Transactions (tdate, ID, tamount)
                            VALUES (%s,%s,%s)""", [last_transaction_date, Id, amount])
            cursor.execute("""
                            Update I
                            SET I.amount = %s + I.amount
                            from Investor as I
                            WHERE I.ID = %s;
                            """, [amount, Id])

        cursor.execute("""select TOP 10 *
                          from Transactions
                          order by tDate desc ,ID desc
                        """)
        sql_res4C = dictfetchall(cursor)  # Update sql_res4 with fetched data
    return render(request, 'Add_Transaction.html', {'sql_res4C': sql_res4C})


def Buy_stocks(request):
    with connection.cursor() as cursor:
        if request.POST:
            Id = request.POST['id']
            company = request.POST['Company']
            quantity = float(request.POST['Quantity'])
            date = last_date(request)

            # check if ID exists in database:
            cursor.execute("""
                            select I.ID
                            from Investor as I
                            where ID = %s
                            """, [Id])
            sql_res5A = dictfetchall(cursor)

            # check if Symbol exists in database:
            cursor.execute("""
                            select C.symbol
                            from Company as C
                            where C.symbol = %s
                            """, [company])
            sql_res5B = dictfetchall(cursor)

            cursor.execute("""
                            select *
                            from Buying as B
                            where B.symbol = %s
                            and B.ID = %s
                            and B.tDate = %s
                            """, [company, Id, date])
            sql_res5C = dictfetchall(cursor)

            # Checking for errors part:
            # check for existence of company and investor
            if (len(sql_res5A) == 0) and (len(sql_res5B) == 0):
                raise Http404(f"Investor with ID {Id} doesn't exists in DB "
                              f"and Company with symbol {company} doesn't exists in DB")

            # Check for existence of Investor:
            if len(sql_res5A) == 0:
                raise Http404(f"Investor with ID {Id} doesn't exists in DB")

            # check for existence of company:
            if len(sql_res5B) == 0:
                raise Http404(f"Company with symbol {company} doesn't exists in DB")

            cursor.execute("""
                            select amount
                            from Investor
                            where ID = %s
                            """, [Id])
            Available_Cash = dictfetchall(cursor)[0]['amount']

            cursor.execute("""
                            select S.Price
                            from Stock S 
                            where S.symbol = %s
                            and S.tDate = %s   
                            """, [company, date])
            Price = dictfetchall(cursor)[0]['Price']

            # check if the investor has not enough money and already bought the stock
            if len(sql_res5C) != 0 and Available_Cash < quantity * Price:
                raise Http404(f"Investor with ID {Id} already bought stock in {date} "
                              f"and the Investor {Id} doesn't have enough money ")

            # check if Investor bought Company's stock in the same day already:
            if len(sql_res5C) != 0:
                raise Http404(f"Investor with ID: {Id} already bought company: {company} stock")

            # check if the investor has not enough money
            if Available_Cash < quantity * Price:
                raise Http404(f"Investor with ID {Id} has not enough available cash")

            # if everything is fine:
            cursor.execute("""
                        INSERT INTO Buying (tDate,ID,Symbol, BQuantity)
                        VALUES (%s,%s,%s,%s)""", [date, Id, company, quantity])

            # update the available cash:
            cursor.execute("""
                            Update I
                            SET I.amount = I.amount - %s
                            from Investor I
                            WHERE I.ID = %s;
                            """, [(quantity * Price), Id])

        # last 10 stocks buy
        cursor.execute("""select TOP 10 *
                          from Buying B
                          order by tDate desc ,ID desc , B.symbol asc 
                        """)
        sql_res5D = dictfetchall(cursor)  # Update sql_res4 with fetched data
    return render(request, 'Buy_Stocks.html', {'sql_res5D': sql_res5D})
