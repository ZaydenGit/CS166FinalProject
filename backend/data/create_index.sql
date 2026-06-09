DROP INDEX IF EXISTS index_bid_auction_id;
DROP INDEX IF EXISTS index_bid_buyer_login;
DROP INDEX IF EXISTS index_payment_buyer_login;
DROP INDEX IF EXISTS index_auction_seller_status;
DROP INDEX IF EXISTS index_pending_shipments;
DROP INDEX IF EXISTS index_bid_history;

CREATE INDEX index_bid_auction_id ON bid(auction_id);

CREATE INDEX index_bid_buyer_login ON bid(buyer_login);

CREATE INDEX index_payment_buyer_login ON payment(buyer_login);

CREATE INDEX index_auction_seller_status ON auction(seller_login, auction_status);

CREATE INDEX index_pending_shipments ON shipment(shipment_status) WHERE shipment_status != 'Delivered';

CREATE INDEX index_bid_history ON bid(auction_id, bid_timestamp DESC); 