class agTransaction:
    def __init__( self ):
        #print( "Creating transaction" )
        self.description            = ""
        self.amount                 = 0.0


class agExpense( agTransaction ):
    def __init__( self ):
        print( "agExpense( amount: amount, description: description )" )
        super( agExpense, self ).__init__() 


class agEarning( agTransaction ):
    def __init__( self ):
        print( "agEarning( amount: amount, description: description )" )
        super( agEarning, self ).__init__()


class agItem:
    def __init__( self ):
        self.description            = "" 
        self.price                  = 0.0
        self.payments               = []

class agBudget:
    def __init__( self ):
        self.money_transactions     = []
        self.items                  = []
       
    def add_expense( self, expense ):
        # type should be agExpense
        if( type( expense ) == agExpense ):
            self.money_transactions.append( expense )
        else:
            raise Exception( 
                    "Trying to add into expenses which is not an expense" )

    def add_earning( self, earning ):
        if( type( earning ) == agEarning ):
            self.money_transactions.append( earning )
        else:
            raise Exception(
                    "Trying to add into earnings which is not an earning" )

    def add_item( self, anItem ):
        self.items.append( anItem )

    def process_payment( self, aPayment ):
        anExpense = agExpense()
        anExpense.amount = aPayment.amount
        
        aPayment.item.payments.append( anExpense )
        
        self.add_item( aPayment.item )
        self.add_expense( anExpense )

class agPayment:
    def __init__( self ):
        print( "agPayment( item: agItem, amount: amount )" )
        self.item = ""
        self.amount = 0.0
