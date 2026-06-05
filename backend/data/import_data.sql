\copy users from './backend/data/users.csv' with delimiter as ';' null '' csv header;
\copy item from './backend/data/items.csv' with delimiter as ';' null '' csv header;
\copy auction from './backend/data/auctions.csv' with delimiter as ';' null '' csv header;
\copy bid from './backend/data/bids.csv' with delimiter as ';' null '' csv header;
\copy shipment from './backend/data/shipments.csv' with delimiter as ';' null '' csv header;
\copy payment from './backend/data/payments.csv' with delimiter as ';' null '' csv header;