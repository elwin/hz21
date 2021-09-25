class Cart:
    def __init__(self, customer_id: int, cart_id: int):
        # YYYYMM, KundeID, WarenkorbID, ProfitKSTID, ProfitKSTNameD, GenossenschaftCode, TransaktionDatumID, TransaktionZeit, ArtikelID, Menge

        self.customer_id = customer_id
        self.cart_id = cart_id
