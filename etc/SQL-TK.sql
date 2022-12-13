create schema sirest_a1;

set search_path to sirest_a1;

create table user_acc (
  email varchar(50) not null,
  password varchar(50) not null,
  phonenum varchar(20) not null,
  fname varchar(15) not null,
  lname varchar(15) not null,
  primary key (email)
);

create table admin (
  email varchar(50) not null,
  primary key (email),
  foreign key (email) references user_acc (email) on delete cascade on update cascade
);

create table transaction_actor(
  email varchar(50) not null,
  nik varchar(20) not null,
  bankname varchar(20) not null,
  accountno varchar(20) not null,
  restopay bigint default 0,
  adminid varchar(50),
  primary key (email),
  foreign key (email) references user_acc (email) on delete cascade on update cascade,
  foreign key (adminid) references admin (email) on delete cascade on update cascade
);

CREATE TABLE COURIER (
  email varchar(50) not null,
  platenum varchar(10) not null,
  drivinglicensenum varchar(20) not null,
  vehicletype varchar(15) not null,
  vehiclebrand varchar(15) not null,
  PRIMARY KEY (email),
  FOREIGN KEY (email) REFERENCES TRANSACTION_ACTOR(email) ON UPDATE CASCADE ON DELETE CASCADE
);

create table customer (
  email varchar(50) not null,
  birthdate date not null,
  sex char(1) not null,
  primary key (email),
  foreign key (email) references transaction_actor (email) on delete cascade on update cascade
);
 
CREATE TABLE RESTAURANT_CATEGORY(
  id varchar(20) not null,
  name varchar(50) not null,
  PRIMARY KEY (id)
);
 
create table restaurant (
  rname varchar(25) not null,
  rbranch varchar(25) not null,
  email varchar(50),
  rphonenum varchar(18) not null,
  street varchar(30) not null,
  district varchar(20) not null,
  city varchar(20) not null,
  province varchar(20) not null,
  rating integer default 0,
  rcategory varchar(20),
  primary key (rname, rbranch),
  foreign key (email) references transaction_actor (email) on delete cascade on update cascade,
  foreign key (rcategory) references restaurant_category (id) on delete cascade on update cascade,
  check (rating >= 0),
  check (rating <= 10)
);
  
create table restaurant_operating_hours (
  name varchar(25) not null,
  branch varchar(25) not null,
  day varchar(10) not null,
  starthours time not null,
  endhours time not null,
  primary key (name, branch, day),
  foreign key (name, branch) references restaurant (rname, rbranch) on delete cascade on update cascade
);

create table food_category(
  id varchar(20) not null,
  name varchar(50) not null,
  primary key (id)
);

create table food(
  rname varchar(25) not null,
  rbranch varchar(25) not null,
  foodname varchar(50) not null,
  description text,
  stock integer not null,
  price bigint not null,
  fcategory varchar(20) not null,
  primary key (rname, rbranch, foodname),
  foreign key (rname, rbranch) references restaurant (rname, rbranch) on delete cascade on update cascade
);
 
CREATE TABLE INGREDIENT(
  id varchar(25) not null,
  name varchar(25) not null,
  PRIMARY KEY (id)
);

CREATE TABLE FOOD_INGREDIENT(
  rname varchar(25) not null,
  rbranch varchar(25) not null,
  foodname varchar(50) not null,
  ingredient varchar(25) not null,
  PRIMARY KEY (rname, rbranch, foodname, ingredient),
  FOREIGN KEY (rname, rbranch, foodname) REFERENCES FOOD (rname, rbranch, foodname) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ingredient) REFERENCES INGREDIENT (id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE PAYMENT_METHOD(
  id varchar(25) not null,
  name varchar(25) not null,
  PRIMARY KEY (id)
);
 
CREATE TABLE PAYMENT_STATUS(
  id varchar(25) not null,
  name varchar(25) not null,
  PRIMARY KEY (id)
);

create table delivery_fee_per_km(
  id varchar(20) not null,
  province varchar(25) not null,
  motorfee int not null,
  carfee int not null,
  primary key (id)
);
 
create table transaction (
  email varchar(50) not null,
  datetime timestamp not null,
  street varchar(30) not null,
  district varchar(30) not null,
  city varchar(25) not null,
  province varchar(25) not null,
  totalfood float not null,
  totaldiscount float not null,
  deliveryfee float not null,
  totalprice float not null,
  rating integer,
  pmid varchar(25) not null,
  psid varchar(25) not null,
  dfid varchar(20) not null,
  courierid varchar(50),
  primary key (email, datetime),
  foreign key (pmid) references payment_method (id) on delete cascade on update cascade,
  foreign key (psid) references payment_status (id) on delete cascade on update cascade,
  foreign key (dfid) references delivery_fee_per_km (id) on delete cascade on update cascade,
  foreign key (courierid) references courier (email) on delete cascade on update cascade
);
 
CREATE TABLE TRANSACTION_STATUS(
  id varchar(25) not null,
  name varchar(40) not null,
  PRIMARY KEY (id)
);

create table transaction_food(
  email varchar(50) not null,
  datetime timestamp not null,
  rname varchar(25) not null,
  rbranch varchar(25) not null,
  foodname varchar(50) not null,
  amount int not null,
  note varchar(255),
  primary key (email, datetime, rname, rbranch, foodname),
  foreign key (email, datetime) references transaction (email, datetime) on delete cascade on update cascade,
  foreign key (rname, rbranch, foodname) references food (rname, rbranch, foodname) on delete cascade on update cascade
);

CREATE TABLE TRANSACTION_HISTORY(
  email varchar(50) not null,
  datetime timestamp not null,
  tsid varchar(25) not null,
  datetimestatus timestamp,
  PRIMARY KEY (email, datetime, tsid),
  FOREIGN KEY (email,datetime) REFERENCES TRANSACTION (email,datetime) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (tsid) REFERENCES TRANSACTION_STATUS (id) ON UPDATE CASCADE ON DELETE CASCADE
);

create table promo (
  id varchar(25) not null,
  promoname varchar(25) not null,
  discount integer not null,
  primary key (id),
  check (discount > 0),
  check (discount <= 100)
);
 
create table min_transaction_promo (
  id varchar(25) not null,
  minimumtransactionnum integer not null,
  primary key (id),
  foreign key (id) references promo (id) on delete cascade on update cascade
);

create table special_day_promo (
  id varchar(25) not null,
  date timestamp not null,
  primary key (id),
  foreign key (id) references promo (id) on delete cascade on update cascade
);

create table restaurant_promo (
  rname varchar(25) not null,
  rbranch varchar(25) not null,
  foodname varchar(50) not null,
  pid varchar(25),
  start_promo timestamp not null,
  end_promo timestamp not null,
  primary key (rname, rbranch),
  foreign key (rname, rbranch, foodname) references food (rname, rbranch, foodname) on delete cascade on update cascade,
  foreign key (pid) references promo (id) on delete cascade on update cascade
);
 
\d USER
\d ADMIN
\d TRANSACTION_ACTOR
\d COURIER
\d CUSTOMER
\d RESTAURANT
\d RESTAURANT_OPERATING_HOURS
\d RESTAURANT_CATEGORY
\d FOOD_CATEGORY
\d FOOD
\d INGREDIENT
\d FOOD_INGREDIENT
\d TRANSACTION
\d DELIVERY_FEE_PER_KM
\d PAYMENT_METHOD
\d PAYMENT_STATUS
\d TRANSACTION_STATUS
\d TRANSACTION_FOOD
\d TRANSACTION_HISTORY
\d PROMO
\d MIN_TRANSACTION_PROMO
\d SPECIAL_DAY_PROMO
\d RESTAURANT_PROMO
 
insert into user_acc values
  ('Tess_Labadie@gmail.com','=,Vel#Y5i0','187391110913120','Tess','Labadie'),
  ('Jayme_Murray@gmail.com','!9Tr/&;FNxUiXb$','8637811956780','Jayme','Murray'),
  ('Prof_William@gmail.com','rdN@}R\wk9^','10011556420181','Prof','William'),
  ('Hector_Gerlach@gmail.com','wMWECU!RYe@','394310888842775','Hector','Gerlach'),
  ('Steve_Rogahn@gmail.com','84`Gx|(w$','6417562136','Steve','Rogahn'),
  ('Dulce_Bashirian@gmail.com','tz$i%BU_Rl.FukZL`o','7511635703','Dulce','Bashirian'),
  ('Savanna_Tillman@gmail.com','7DOM`uDz8WJNhuF%$r','6723844081','Savanna','Tillman'),
  ('Kelton_Gorczany@gmail.com','TA?%kLiUH^p%x3+ci)','4981676376','Kelton','Gorczany'),
  ('Vergie_Grimes@gmail.com','MPx^$ZuI)I(}8.f,@mT','330600655279527','Vergie','Grimes'),
  ('Prof_Brennon@gmail.com','4s@W0WC=CZZ','81394164654913','Prof','Brennon'),
  ('Elfrieda_Wilderman@gmail.com','L[V%S:(Zf.c!F}zl','08037314871','Elfrieda','Wilderman'),
  ('Eula_Mayert@gmail.com','OGt:k+QNYHaP=-[','13058346522','Eula','Mayert'),
  ('Hosea_Swaniawski@gmail.com','h%sC+?bv`7%y]$!+[','9666646214','Hosea','Swaniawski'),
  ('Veda_Watsica@gmail.com','v6*wrD7k%qE6ZT)','16650313125','Veda','Watsica'),
  ('Edyth_Lindgren@gmail.com','+FqU$VKv?{c4','7840484406','Edyth','Lindgren'),
  ('Mr_Kaleb@gmail.com','XbCj2]HaHo_GB9Rt^','06405529831','Mr','Kaleb'),
  ('General_Brekke@gmail.com',':W(OU#&fgN#xE','934396778485938','General','Brekke'),
  ('Ms_Adell@gmail.com','cBexgjy%eNNs','171066371771175','Ms','Adell'),
  ('Orpha_Leannon@gmail.com','qwRj$"Z?"#{Nix','094782183032129','Orpha','Leannon'),
  ('Mr_Karl@gmail.com','js)69.WM:','7409848604604','Mr','Karl'),
  ('Andreanne_Johnson@gmail.com','*|@421Q28m4ea:CSuV','5510849680','Andreanne','Johnson'),
  ('Prof_Darrell@gmail.com','tVGk4zM9FF','337737866307916','Prof','Darrell'),
  ('Shaina_Barton@gmail.com',')22zg`0~@W%i!=/6','6278279372238','Shaina','Barton'),
  ('Mr_Curt@gmail.com','[TBRjIto#FaZH`Ri','146790602884309','Mr','Curt'),
  ('Taya_King@gmail.com','Pa5xmusz0B7h8Zj','5984909264771','Taya','King'),
  ('Ms_Zola@gmail.com','[6?)X*Cf:0.NA0','06123025469','Ms','Zola'),
  ('Curt_Schneider@gmail.com','0_9g*H0v[FE','8731439350273','Curt','Schneider'),
  ('Jovani_Ernser@gmail.com','KuDSG_-+h','1624654063684','Jovani','Ernser'),
  ('Prof_Maddison@gmail.com','8l8,Q$7Pq,N;K-IAB','5279956558290','Prof','Maddison'),
  ('Soledad_Doyle@gmail.com','v1_K9;5FkhV0{','232808755497898','Soledad','Doyle'),
  ('Nyah_Oberbrunner@gmail.com','M56?_b\DX-;SFw;"T','02979583386','Nyah','Oberbrunner'),
  ('Nella_Jerde@gmail.com','|$PaXKH''39:','9506499550223','Nella','Jerde'),
  ('Chet_Wintheiser@gmail.com','JF!Sg.fdZO\x;@|-zQJ','184034183421606','Chet','Wintheiser'),
  ('Miss_Elaina@gmail.com','EazHex,*Dk!~G]-','8413666923','Miss','Elaina'),
  ('John_Christiansen@gmail.com','IG*"p^(@Y:gcm+J;df','65700203420265','John','Christiansen'),
  ('Bonita_Thompson@gmail.com','f?hlJ(U0$[~:,','7869788093541','Bonita','Thompson'),
  ('Mr_Salvador@gmail.com','WNb#`~BJt9Q,J4s31al7','1578791143879','Mr','Salvador'),
  ('Dr_Quinton@gmail.com','ID;AGsdFGLXj`8','9483213388','Dr.','Quinton'),
  ('Raleigh_Murray@gmail.com','EA;g%-ADYd0k-L8vS?l','10503937743898','Raleigh','Murray'),
  ('Ms_Treva@gmail.com','~K}g(p4-j{/','11371669547','Ms','Treva'),
  ('Nasir_Greenfelder@gmail.com','hmM2`TbwiTz@=f,b#H','33073958265739','Nasir','Greenfelder'),
  ('Aurelie_Rolfson@gmail.com','n*kcpnqKR24','169921524633206','Aurelie','Rolfson'),
  ('Felicia_Weber@gmail.com','9adW,usg"Wc}Y?d','2101664122476','Felicia','Weber'),
  ('Mrs_Bernadine@gmail.com','WT''vcZ$D5l""@W7~Qnn[t','14773454037','Mrs','Bernadine'),
  ('Bonnie_Little@gmail.com','muG)m]q/Z$l|','2800811231','Bonnie','Little');
 
insert into admin values
  ('Tess_Labadie@gmail.com'),
  ('Jayme_Murray@gmail.com'),
  ('Prof_William@gmail.com'),
  ('Hector_Gerlach@gmail.com'),
  ('Steve_Rogahn@gmail.com');

insert into transaction_actor values
  ('Dulce_Bashirian@gmail.com','9018344908528880','Mandiri','BR002','12500','Tess_Labadie@gmail.com'),
  ('Savanna_Tillman@gmail.com','3324396477521421','BNI','BR003','14000','Jayme_Murray@gmail.com'),
  ('Kelton_Gorczany@gmail.com','3537085869758208','BCA','BR004','11500','Jayme_Murray@gmail.com'),
  ('Vergie_Grimes@gmail.com','9816226837961717','Mandiri','MT001','8000','Prof_William@gmail.com'),
  ('Prof_Brennon@gmail.com','1373111413809307','BNI','MT002','15000','Hector_Gerlach@gmail.com'),
  ('Elfrieda_Wilderman@gmail.com','2223509872730385','BRI','MT003','9000','Steve_Rogahn@gmail.com'),
  ('Eula_Mayert@gmail.com','1723561993508037','BCA','MT004','17000','Tess_Labadie@gmail.com'),
  ('Hosea_Swaniawski@gmail.com','3407707125351288','BRI','RB001','20500','Jayme_Murray@gmail.com'),
  ('Veda_Watsica@gmail.com','1663046385997304','Mandiri','RB002','22000','Prof_William@gmail.com'),
  ('Edyth_Lindgren@gmail.com','3110181921568232','BNI','RB003','21000','Hector_Gerlach@gmail.com'),
  ('Mr_Kaleb@gmail.com','3059891267826887','BRI','RB004','16500','Steve_Rogahn@gmail.com'),
  ('General_Brekke@gmail.com','7012213860777765','BNI','RM001','16000','Tess_Labadie@gmail.com'),
  ('Ms_Adell@gmail.com','2340615048226353','BCA','RM002','34000','Jayme_Murray@gmail.com'),
  ('Orpha_Leannon@gmail.com','0797607930131113','Mandiri','RM003','1500','Prof_William@gmail.com'),
  ('Mr_Karl@gmail.com','5745855617446235','BRI','RM004','9500','Hector_Gerlach@gmail.com'),
  ('Andreanne_Johnson@gmail.com','42703845016475266158','Mandiri','RM006','20000', 'Tess_Labadie@gmail.com'),
  ('Prof_Darrell@gmail.com','46974178329240038033','BCA','MT005','50000', 'Tess_Labadie@gmail.com'),
  ('Shaina_Barton@gmail.com','72262127611266802716','BNI','RB005','15000','Prof_William@gmail.com'),
  ('Mr_Curt@gmail.com','30205492886262411819','Mandiri','RM005','4000', 'Jayme_Murray@gmail.com'),
  ('Taya_King@gmail.com','65904162292638911052','BNI','RB006','20000','Prof_William@gmail.com'),
  ('Ms_Zola@gmail.com','68338839412557097781','BCA','MT006','13000', 'Tess_Labadie@gmail.com'),
  ('Curt_Schneider@gmail.com','35741649915804395378','BRI','BR005','16000', 'Jayme_Murray@gmail.com'),
  ('Jovani_Ernser@gmail.com','04177630259399916881','Mandiri','RM007','10000','Prof_William@gmail.com'),
  ('Prof_Maddison@gmail.com','87586120031200040045','BCA','MT007','13000','Hector_Gerlach@gmail.com'),
  ('Soledad_Doyle@gmail.com','78071587957288351977','Mandiri','RM008','7000', 'Tess_Labadie@gmail.com'),
  ('Nyah_Oberbrunner@gmail.com','51946968159264102356','Mandiri','RM009','8000', 'Jayme_Murray@gmail.com'),
  ('Nella_Jerde@gmail.com','54127132969262007269','BCA','MT008','14000','Steve_Rogahn@gmail.com'),
  ('Chet_Wintheiser@gmail.com','74587933910040520310','BCA','MT009','7000','Hector_Gerlach@gmail.com'),
  ('Miss_Elaina@gmail.com','45489396943970697372','BNI','RB007','18000', 'Jayme_Murray@gmail.com'),
  ('John_Christiansen@gmail.com','80982325785464129540','BNI','RB008','21000', 'Jayme_Murray@gmail.com'),
  ('Bonita_Thompson@gmail.com','00611165390737981617','Mandiri','RM010','5000', 'Tess_Labadie@gmail.com'),
  ('Mr_Salvador@gmail.com','50271045036449121288','BRI','BR006','30000','Jayme_Murray@gmail.com'),
  ('Dr_Quinton@gmail.com','94319950739126463252','BNI','RB009','13000','Hector_Gerlach@gmail.com'),
  ('Raleigh_Murray@gmail.com','15892730290715149659','BRI','BR007','18000','Steve_Rogahn@gmail.com'),
  ('Ms_Treva@gmail.com','68047852064081722873','Mandiri','RM011','15000','Prof_William@gmail.com'),
  ('Nasir_Greenfelder@gmail.com','37611679018539463251','BRI','BR008','9000', 'Tess_Labadie@gmail.com'),
  ('Aurelie_Rolfson@gmail.com','44100580314786331994','BCA','MT010','19000','Hector_Gerlach@gmail.com'),
  ('Felicia_Weber@gmail.com','12698903068185179977','BNI','RB010','20000','Jayme_Murray@gmail.com'),
  ('Mrs_Bernadine@gmail.com','33490310360694478848','BRI','BR009','17000','Prof_William@gmail.com'),
  ('Bonnie_Little@gmail.com','71086318189497933546','Mandiri','RM012','12500','Hector_Gerlach@gmail.com');

-- Update vehicletype and vehiclebrand
insert into courier values
  ('Dulce_Bashirian@gmail.com','BPKJ07','00000000000003','Mobil','Toyota'),
  ('Savanna_Tillman@gmail.com','F91LGN','00000000000006','Motor ','Suzuki'),
  ('Kelton_Gorczany@gmail.com','4HQN216','00000000000007','Motor','Honda'),
  ('Vergie_Grimes@gmail.com','DCK7853','00000000000008','Mobil','Chevrolet'),
  ('Prof_Brennon@gmail.com','5RIN076','00000000000011','Mobil','Ford'),
  ('Elfrieda_Wilderman@gmail.com','A22YUX','00000000000002','Mobil','Toyota'),
  ('Eula_Mayert@gmail.com','B0ZCWE','00000000000012','Motor','Yamaha'),
  ('Hosea_Swaniawski@gmail.com','S8B387','00000000000005','Mobil','Honda'),
  ('Veda_Watsica@gmail.com','IS1CKB','00000000000020','Motor','Honda'),
  ('Edyth_Lindgren@gmail.com','U9R9RL','00000000000017','Motor','Yamaha');

insert into customer values
  ('Andreanne_Johnson@gmail.com','1991-06-03','F'),
  ('Prof_Darrell@gmail.com','1970-02-27','M'),
  ('Shaina_Barton@gmail.com','1993-05-17','F'),
  ('Mr_Curt@gmail.com','2007-01-27','M'),
  ('Taya_King@gmail.com','1997-12-13','F'),
  ('Ms_Zola@gmail.com','1998-02-01','F'),
  ('Curt_Schneider@gmail.com','1979-04-17','F'),
  ('Jovani_Ernser@gmail.com','1984-08-26','M'),
  ('Prof_Maddison@gmail.com','1981-09-23','F'),
  ('Soledad_Doyle@gmail.com','2007-05-08','M'),
  ('Nyah_Oberbrunner@gmail.com','2000-10-02','M'),
  ('Nella_Jerde@gmail.com','1988-09-10','F'),
  ('Chet_Wintheiser@gmail.com','1981-06-21','M'),
  ('Miss_Elaina@gmail.com','1995-11-24','F'),
  ('John_Christiansen@gmail.com','1995-09-15','M'),
  ('Mr_Kaleb@gmail.com','1988-12-07','M'),
  ('General_Brekke@gmail.com','2003-05-01','M'),
  ('Ms_Adell@gmail.com','1989-08-08','F'),
  ('Orpha_Leannon@gmail.com','2006-01-09','F'),
  ('Mr_Karl@gmail.com','1992-08-28','M');

insert into restaurant_category values
  ('00000000000000000000','Japanese'),
  ('00000000000000000001','Western'),
  ('00000000000000000002','Chinese'),
  ('00000000000000000003','Indian'),
  ('00000000000000000004','Vietnamese');

insert into restaurant values
  ('Harlequin','Louisville','Bonita_Thompson@gmail.com','106247838632919','Jl. Pemuda no. 31','Rawamangun','Jakarta Timur','DKI Jakarta','4','00000000000000000000'),
  ('The King''s Empress','Fayetteville','Mr_Salvador@gmail.com','16908104443210','Jl. Malioboro no. 22','Danurejan','Yogyakarta','DIY Yogyakarta','1','00000000000000000003'),
  ('The Eastern Mockingbird','Fayetteville','Dr_Quinton@gmail.com','6821572724','Jl. Kartini no. 77','Kejaksan','Cirebon','Jawa Barat','5','00000000000000000001'),
  ('The Shining Way','Washington','Raleigh_Murray@gmail.com','199532973539286','Jl. M. H. Thamrin no. 42','Menteng','Jakarta Pusat','DKI Jakarta','10','00000000000000000003'),
  ('The Underwater Garden','Manchester','Ms_Treva@gmail.com','3514009802685','Jl. DR. Soedarso No. 1','Pontianak Tenggara','Pontianak','Kalimantan Barat','3','00000000000000000001'),
  ('The Japanese Bites','Panama City','Nasir_Greenfelder@gmail.com','3539088768760','Jl. Perintis no. 3','Sesayap','Tarakan','Kalimantan Utara','8','00000000000000000001'),
  ('The Bamboo Road','Port Wentworth','Aurelie_Rolfson@gmail.com','02553967571','Jl. Dg. Ngeppe no. 51','Tamalate','Makassar','Sulawesi Selatan','1','00000000000000000000'),
  ('The Pink Rooftop','Woburn','Felicia_Weber@gmail.com','106158275883624','Jl. Dago no 90','Coblong','Bandung','Jawa Barat','4','00000000000000000002'),
  ('Oddity','Manchester','Mrs_Bernadine@gmail.com','1736890390153','Jl. Margonda no. 33','Beji','Depok','Jawa Barat','8','00000000000000000000'),
  ('The Court Door','Nashville','Bonnie_Little@gmail.com','4371025246','Jl. Dr.Sutomo No. 42','Batang','Batang','Jawa Tengah','5','00000000000000000002');

insert into restaurant_operating_hours values
  ('Harlequin','Louisville','Senin','00:00:00','12:00:00'),
  ('The King''s Empress','Fayetteville','Selasa','06:00:00','20:00:00'),
  ('The Eastern Mockingbird','Fayetteville','Rabu','00:00:00','10:00:00'),
  ('The Shining Way','Washington','Kamis','00:00:00','17:00:00'),
  ('The Underwater Garden','Manchester','Jumat','17:00:00','23:00:00'),
  ('The Japanese Bites','Panama City','Senin','07:00:00','12:00:00'),
  ('The Bamboo Road','Port Wentworth','Selasa','00:00:00','12:00:00'),
  ('The Pink Rooftop','Woburn','Rabu','00:00:00','15:00:00'),
  ('Oddity','Manchester','Kamis','12:00:00','00:00:00'),
  ('The Court Door','Nashville','Jumat','00:00:00','09:00:00');
 
insert into food_category values
  ('00000000000000000000','Seafood'),
  ('00000000000000000001','Chinese food'),
  ('00000000000000000002','Western food'),
  ('00000000000000000003','Indonesian food'),
  ('00000000000000000004','Japanese food');
 
insert into food values
  ('The Court Door','Nashville','Grapefruit and egg ciabatta','Warm ciabatta filled with pink grapefruit and free range eggs','7','300000','00000000000000000000'),
  ('The Court Door','Nashville','Anise and crab korma','Creamy korma made with fresh anise and crab','5','300000','00000000000000000000'),
  ('The Court Door','Nashville','Squirrel and thai basil salad','Squirrel and fresh thai basil served on a bed of lettuce','16','300000','00000000000000000000'),
  ('The Japanese Bites','Panama City','Lamb and shrimp soup','Minced lamb and shrimp combined into smooth soup','7','300000','00000000000000000000'),
  ('The Japanese Bites','Panama City','Banana and thyme pancake','Crispy pancake filled with fresh banana and thyme','26','300000','00000000000000000000'),
  ('The Japanese Bites','Panama City','Chicken and squash skewers','Bamboo skewers loaded with corn-fed chicken and pattypan squash','37','300000','00000000000000000000'),
  ('The King''s Empress','Fayetteville','Blueberry and pear pancake','Crispy pancake filled with fresh blueberry and juicy pears','27','700000','00000000000000000001'),
  ('The King''s Empress','Fayetteville','Crunch Crunch','Crunchy stir fry featuring fresh okra and anise','17','700000','00000000000000000001'),
  ('The King''s Empress','Fayetteville','Plumcot and pollack salad','Fresh plumcot and pollack served on a bed of lettuce','18','700000','00000000000000000001'),
  ('The Eastern Mockingbird','Fayetteville','Aubergine and spinach dumplings','Thin pastry cases stuffed with marinaded aubergine and baby spinach','19','700000','00000000000000000001'),
  ('The Eastern Mockingbird','Fayetteville','Thickie Spagettie','Spagetti topped with a blend of thick bacon and fresh pepper','6','700000','00000000000000000001'),
  ('The Eastern Mockingbird','Fayetteville','Squash and karengo soup','Acorn squash and karengo combined into creamy soup','8','700000','00000000000000000001'),
  ('The Underwater Garden','Manchester','Tomato and bean soup','Beef tomatoes and bean combined into chunky soup','6','1600000','00000000000000000002'),
  ('The Underwater Garden','Manchester','Mortadella and hp sauce salad','A crisp salad featuring mortadella and hp sauce','27','1600000','00000000000000000002'),
  ('The Underwater Garden','Manchester','Udon and juniper berry salad','A crisp salad featuring udon and fresh juniper berry','11','1600000','00000000000000000002'),
  ('The Bamboo Road','Port Wentworth','Peppercorn and pumpkin soup','Black peppercorn and spiced pumpkin combined into chunky soup','30','1600000','00000000000000000002'),
  ('The Bamboo Road','Port Wentworth','Stilton and cider vinegar salad','A crisp salad featuring stilton and cider vinegar','7','1600000','00000000000000000002'),
  ('The Bamboo Road','Port Wentworth','Black pepper and fish ciabatta','Warm ciabatta filled with crushed black pepper and fish','9','1600000','00000000000000000002'),
  ('Oddity','Manchester','Garam masala and fish gyoza','Thin pastry cases stuffed with garam masala and fish','22','170000','00000000000000000003'),
  ('Oddity','Manchester','Tofu and black pepper toastie','Crisp slices of bread filled with silken tofu and crushed black pepper','14','170000','00000000000000000003'),
  ('Oddity','Manchester','Bacon and olive penne','Fresh egg tubular pasta in a sauce made from lea bacon and olive','25','170000','00000000000000000003'),
  ('The Shining Way','Washington','Cocoa and milk pudding','A rich suet pudding made with cocoa and semi-skimmed milk','12','170000','00000000000000000003'),
  ('The Shining Way','Washington','Pork and tumeric vindaloo','Hot vindaloo made with pork and tumeric','10','170000','00000000000000000003'),
  ('The Shining Way','Washington','Tongue and wheat bran salad','Tongue and wheat bran served on a bed of lettuce','17','170000','00000000000000000003'),
  ('Harlequin','Louisville','Peach and sultana cookies','Crunchy cookies made with fresh peach and sultana','16','1100000','00000000000000000004'),
  ('Harlequin','Louisville','Prune and pumpkin buns','Crumbly buns made with fresh prune and spiced pumpkin','5','1100000','00000000000000000004'),
  ('Harlequin','Louisville','Pumpkin and pepper curry','Spicy curry made with spiced pumpkin and baby pepper','13','1100000','00000000000000000004'),
  ('The Pink Rooftop','Woburn','Rosemary and squash buns','Moist buns made with fresh rosemary and pattypan squash','17','1100000','00000000000000000004'),
  ('The Pink Rooftop','Woburn','Borscht and feta soup','Borscht and tangy feta combined into chunky soup','9','1100000','00000000000000000004'),
  ('The Pink Rooftop','Woburn','Leek and sausage pasta','Fresh egg pasta in a sauce made from frizzled leek and Cumberland sausage','8','1100000','00000000000000000004');
 
insert into transaction_status values
  ('0000000000000000000000000','Menunggu konfirmasi restoran'),
  ('0000000000000000000000001','Pesanan sedang dipersiapkan'),
  ('0000000000000000000000002','Pesanan dalam perjalanan'),
  ('0000000000000000000000003','Pesanan sudah diantar'),
  ('0000000000000000000000004','Pesanan selesai'),
  ('0000000000000000000000005','Pesanan dibatalkan');

insert into delivery_fee_per_km values
  ('00000000000000000000','DKI Jakarta','10000','20000'),
  ('00000000000000000001','DIY Yogyakarta','8000','15000'),
  ('00000000000000000002','Jawa Barat','7500','12500'),
  ('00000000000000000003','Jawa Tengah','8500','15500'),
  ('00000000000000000004','Jawa Timur','9500','17500'),
  ('00000000000000000005','Kalimantan Barat','7000','12000'),
  ('00000000000000000006','Kalimantan Utara','8000','13000'),
  ('00000000000000000007','Sulawesi Selatan','9000','25000'),
  ('00000000000000000008','Kalimantan Tengah','12000','22000'),
  ('00000000000000000009','Nanggroe Aceh Darussalam','12000','22000');

insert into promo values
  ('000000000000000','promoharibesar','10'),
  ('000000000000001','promoultah','20'),
  ('000000000000002','promokamis','15'),
  ('000000000000003','promotanggalmerah','10'),
  ('000000000000004','promotahunbaru','25'),
  ('000000000000005','promolebaran','70'),
  ('000000000000006','promotanggalkembar','80'),
  ('000000000000007','promojam8','10'),
  ('000000000000008','promoharijumat','15'),
  ('000000000000009','promomakanber10','15'),
  ('000000000000010','promotransaksipertama','10'),
  ('000000000000011','promoloyal3kali','15'),
  ('000000000000012','promoloyal5kali','20'),
  ('000000000000013','promo10kali','25'),
  ('000000000000014','promo20kali','27'),
  ('000000000000015','promo30kali','30'),
  ('000000000000016','promo50kali','40'),
  ('000000000000017','promo70kali','50'),
  ('000000000000018','promocomeback','20'),
  ('000000000000019','promo100kali','75');

insert into special_day_promo values
  ('000000000000000','2022-10-10'),
  ('000000000000001','2022-09-09'),
  ('000000000000002','2022-01-01'),
  ('000000000000003','2022-02-02'),
  ('000000000000004','2022-03-03'),
  ('000000000000005','2022-04-04'),
  ('000000000000006','2022-05-05'),
  ('000000000000007','2022-06-06'),
  ('000000000000008','2022-07-07'),
  ('000000000000009','2022-08-08');

insert into min_transaction_promo values
  ('000000000000010',1),
  ('000000000000011',3),
  ('000000000000012',5),
  ('000000000000013',10),
  ('000000000000014',20),
  ('000000000000015',30),
  ('000000000000016',50),
  ('000000000000017',70),
  ('000000000000018',2),
  ('000000000000019',100);

insert into ingredient values
  ('0000000000000000000000000','fennel seed'),
  ('0000000000000000000000001','garlic powder'),
  ('0000000000000000000000002','cranberry'),
  ('0000000000000000000000003','lemonade'),
  ('0000000000000000000000004','cantaloupe'),
  ('0000000000000000000000005','soy milk'),
  ('0000000000000000000000006','passion fruit'),
  ('0000000000000000000000007','kiwi fruit'),
  ('0000000000000000000000008','lemonade'),
  ('0000000000000000000000009','walnut'),
  ('0000000000000000000000010','mustard seeds'),
  ('0000000000000000000000011','salsa'),
  ('0000000000000000000000012','saffron'),
  ('0000000000000000000000013','walnut'),
  ('0000000000000000000000014','snap pea'),
  ('0000000000000000000000015','cornmeal'),
  ('0000000000000000000000016','cilantro'),
  ('0000000000000000000000017','zinfandel wine'),
  ('0000000000000000000000018','strawberry'),
  ('0000000000000000000000019','cranberry');

insert into payment_method values
  ('0000000000000000000000000','Credit card'),
  ('0000000000000000000000001','RestoPay'),
  ('0000000000000000000000002','Cash'),
  ('0000000000000000000000003','Debit cards'),
  ('0000000000000000000000004','Electronic bank transfers');

insert into payment_status values
  ('0000000000000000000000000','Menunggu pembayaran'),
  ('0000000000000000000000001','Berhasil'),
  ('0000000000000000000000002','Dibatalkan');
  ('0000000000000000000000003','Gagal');

insert into restaurant_promo values
  ('Harlequin','Louisville','Prune and pumpkin buns','000000000000000','2022-10-10','2022-10-17'),
  ('The King''s Empress','Fayetteville','Crunch Crunch','000000000000001','2022-09-09','2022-09-14'),
  ('The Eastern Mockingbird','Fayetteville','Aubergine and spinach dumplings','000000000000015','2022-01-01','2022-01-04'),
  ('The Shining Way','Washington','Tongue and wheat bran salad','000000000000003','2022-02-02','2022-02-05'),
  ('The Underwater Garden','Manchester','Udon and juniper berry salad','000000000000004','2022-03-03','2022-03-06'),
  ('The Japanese Bites','Panama City','Chicken and squash skewers','000000000000005','2022-04-04','2022-04-07'),
  ('The Bamboo Road','Port Wentworth','Black pepper and fish ciabatta','000000000000012','2022-05-05','2022-05-08'),
  ('The Pink Rooftop','Woburn','Rosemary and squash buns','000000000000007','2022-06-06','2022-06-09'),
  ('Oddity','Manchester','Tofu and black pepper toastie','000000000000011','2022-07-07','2022-07-10'),
  ('The Court Door','Nashville','Grapefruit and egg ciabatta','000000000000009','2022-08-08','2022-08-12');

insert into food_ingredient values
  ('The Court Door','Nashville','Grapefruit and egg ciabatta','0000000000000000000000007'),
  ('The Court Door','Nashville','Anise and crab korma','0000000000000000000000008'),
  ('The Court Door','Nashville','Squirrel and thai basil salad','0000000000000000000000016'),
  ('The Japanese Bites','Panama City','Lamb and shrimp soup','0000000000000000000000007'),
  ('The Japanese Bites','Panama City','Banana and thyme pancake','0000000000000000000000014'),
  ('The Japanese Bites','Panama City','Chicken and squash skewers','0000000000000000000000006'),
  ('The King''s Empress','Fayetteville','Blueberry and pear pancake','0000000000000000000000013'),
  ('The King''s Empress','Fayetteville','Crunch Crunch','0000000000000000000000008'),
  ('The King''s Empress','Fayetteville','Plumcot and pollack salad','0000000000000000000000014'),
  ('The Eastern Mockingbird','Fayetteville','Aubergine and spinach dumplings','0000000000000000000000004'),
  ('The Eastern Mockingbird','Fayetteville','Thickie Spagettie','0000000000000000000000016'),
  ('The Eastern Mockingbird','Fayetteville','Squash and karengo soup','0000000000000000000000000'),
  ('The Underwater Garden','Manchester','Tomato and bean soup','0000000000000000000000016'),
  ('The Underwater Garden','Manchester','Mortadella and hp sauce salad','0000000000000000000000002'),
  ('The Underwater Garden','Manchester','Udon and juniper berry salad','0000000000000000000000017'),
  ('The Bamboo Road','Port Wentworth','Peppercorn and pumpkin soup','0000000000000000000000019'),
  ('The Bamboo Road','Port Wentworth','Stilton and cider vinegar salad','0000000000000000000000002'),
  ('The Bamboo Road','Port Wentworth','Black pepper and fish ciabatta','0000000000000000000000014'),
  ('Oddity','Manchester','Garam masala and fish gyoza','0000000000000000000000009'),
  ('Oddity','Manchester','Tofu and black pepper toastie','0000000000000000000000013'),
  ('Oddity','Manchester','Bacon and olive penne','0000000000000000000000009'),
  ('The Shining Way','Washington','Cocoa and milk pudding','0000000000000000000000015'),
  ('The Shining Way','Washington','Pork and tumeric vindaloo','0000000000000000000000001'),
  ('The Shining Way','Washington','Tongue and wheat bran salad','0000000000000000000000006'),
  ('Harlequin','Louisville','Peach and sultana cookies','0000000000000000000000010'),
  ('Harlequin','Louisville','Prune and pumpkin buns','0000000000000000000000009'),
  ('Harlequin','Louisville','Pumpkin and pepper curry','0000000000000000000000005'),
  ('The Pink Rooftop','Woburn','Rosemary and squash buns','0000000000000000000000012'),
  ('The Pink Rooftop','Woburn','Borscht and feta soup','0000000000000000000000017'),
  ('The Pink Rooftop','Woburn','Leek and sausage pasta','0000000000000000000000006');
 

insert into transaction values
  ('Curt_Schneider@gmail.com','2022-03-21 13:23:44','Jl. Taman Apel','Kembangan','Jakarta Barat','DKI Jakarta','10','20.5','8.500','60.000','7','0000000000000000000000000','0000000000000000000000000','00000000000000000000','Dulce_Bashirian@gmail.com'),
  ('Prof_Darrell@gmail.com', '2022-12-23 13:21:44','Jl. Taman Anggur','Kembangan','Jakarta Barat','DKI Jakarta','9','25.5','8.500','80.000','9','0000000000000000000000001','0000000000000000000000000','00000000000000000000','Savanna_Tillman@gmail.com'),
  ('Taya_King@gmail.com', '2022-11-24 13:22:44','Jl. Taman Jeruk','Kembangan','Jakarta Barat','DKI Jakarta','11','30.5','8.500','70.000','8','0000000000000000000000001','0000000000000000000000000','00000000000000000000','Kelton_Gorczany@gmail.com'),
  ('Shaina_Barton@gmail.com', '2022-10-25 13:26:44','Jl. Taman Mangga','Kembangan','Jakarta Barat','DKI Jakarta','12','40.5','8.500','90.000','7','0000000000000000000000000','0000000000000000000000000','00000000000000000000','Vergie_Grimes@gmail.com'),
  ('Mr_Curt@gmail.com', '2022-09-26 13:27:44','Jl. Taman Alpukat','Kembangan','Jakarta Barat','DKI Jakarta','8','45.5','8.500','80.000','8','0000000000000000000000002','0000000000000000000000000','00000000000000000000','Prof_Brennon@gmail.com'),
  ('Prof_Maddison@gmail.com','2022-08-27 14:23:44','Jl. Taman Sirsak','Kembangan','Jakarta Barat','DKI Jakarta','12','50.5','8.500','80.000','5','0000000000000000000000001','0000000000000000000000000','00000000000000000000','Elfrieda_Wilderman@gmail.com'),
  ('Ms_Zola@gmail.com','2022-07-28 15:23:44','Jl. Taman Belimbing','Kembangan','Jakarta Barat','DKI Jakarta','13','75.5','8.500','70.000','9','0000000000000000000000002','0000000000000000000000000','00000000000000000000','Eula_Mayert@gmail.com'),
  ('Jovani_Ernser@gmail.com','2022-06-29 16:23:44','Jl. Gatot Subroto','Kembangan','Jakarta Barat','DKI Jakarta','14','15.5','8.500','80.000','9','0000000000000000000000001','0000000000000000000000000','00000000000000000000','Hosea_Swaniawski@gmail.com'),
  ('John_Christiansen@gmail.com','2022-05-11 17:23:44','Jl. Taman Asri','Kembangan','Jakarta Barat','DKI Jakarta','11','20.5','8.500','65.000','7','0000000000000000000000002','0000000000000000000000000','00000000000000000000','Veda_Watsica@gmail.com'),
  ('Soledad_Doyle@gmail.com','2022-04-12 18:23:44','Jl. Taman Yakult','Kembangan','Jakarta Barat','DKI Jakarta','15','35.5','8.500','85.000','6','0000000000000000000000000','0000000000000000000000000','00000000000000000000','Savanna_Tillman@gmail.com');
 
insert into transaction_food values
  ('Curt_Schneider@gmail.com','2022-03-21 13:23:44','The Court Door','Nashville','Grapefruit and egg ciabatta',5,''),
  ('Prof_Darrell@gmail.com', '2022-12-23 13:21:44','The Court Door','Nashville','Anise and crab korma',12,'Extra sauce please'),
  ('Taya_King@gmail.com', '2022-11-24 13:22:44','The Court Door','Nashville','Squirrel and thai basil salad',8,'Less sugar'),
  ('Shaina_Barton@gmail.com', '2022-10-25 13:26:44','The Japanese Bites','Panama City','Lamb and shrimp soup',12,'No chili'),
  ('Mr_Curt@gmail.com', '2022-09-26 13:27:44','The Japanese Bites','Panama City','Banana and thyme pancake',9,'No chili'),
  ('Prof_Maddison@gmail.com','2022-08-27 14:23:44','The Japanese Bites','Panama City','Chicken and squash skewers',0,'Less sugar'),
  ('Ms_Zola@gmail.com','2022-07-28 15:23:44','The King''s Empress','Fayetteville','Blueberry and pear pancake',8,'Extra sauce please'),
  ('Jovani_Ernser@gmail.com','2022-06-29 16:23:44','The King''s Empress','Fayetteville','Crunch Crunch',6,'No chili'),
  ('John_Christiansen@gmail.com','2022-05-11 17:23:44','The King''s Empress','Fayetteville','Plumcot and pollack salad',8,'Extra sauce please'),
  ('Soledad_Doyle@gmail.com','2022-04-12 18:23:44','The Eastern Mockingbird','Fayetteville','Aubergine and spinach dumplings',10,'Less sugar');

insert into transaction_history values
  ('Curt_Schneider@gmail.com','2022-03-21 13:23:44','0000000000000000000000000','2022-03-21 13:24:44'),
  ('Prof_Darrell@gmail.com', '2022-12-23 13:21:44','0000000000000000000000002','2022-12-23 13:23:44'),
  ('Taya_King@gmail.com', '2022-11-24 13:22:44','0000000000000000000000001','2022-11-24 13:23:24'),
  ('Shaina_Barton@gmail.com', '2022-10-25 13:26:44','0000000000000000000000003','2022-10-25 13:27:44'),
  ('Mr_Curt@gmail.com', '2022-09-26 13:27:44','0000000000000000000000001','2022-09-26 13:28:44'),
  ('Prof_Maddison@gmail.com','2022-08-27 14:23:44','0000000000000000000000001','2022-08-27 14:24:44'),
  ('Ms_Zola@gmail.com','2022-07-28 15:23:44','0000000000000000000000003','2022-07-28 15:24:34'),
  ('Jovani_Ernser@gmail.com','2022-06-29 16:23:44','0000000000000000000000002','2022-06-29 16:25:54'),
  ('John_Christiansen@gmail.com','2022-05-11 17:23:44','0000000000000000000000004','2022-05-11 17:24:44'),
  ('Soledad_Doyle@gmail.com','2022-04-12 18:23:44','0000000000000000000000002','2022-04-12 18:25:44');

-- Trigger 1

create or replace function checkPassword() 
returns trigger as
$$
  begin
    if (tg_op = 'INSERT' or tg_op = 'UPDATE') then
      if (not (new.password ~ '(?=.*\d)(?=.*[A-Z])')) then
        raise exception 'Password must contain at least 1 uppercase and 1 number';
      end if;
      return new;
    end if;
  end;
$$
language plpgsql; 

create trigger triggerCheckPassword
before insert or update on user_acc
for each row
execute procedure checkPassword();

-- Trigger 2 (kenneth)

CREATE OR REPLACE FUNCTION checkSaldoRestoPay()
RETURNS trigger AS
$$
	DECLARE 
		saldoRestoPay bigint;
	BEGIN
		IF(TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
      IF (NEW.pmid = '0000000000000000000000001') then
        SELECT restopay into saldoRestoPay
        FROM transaction_actor
        WHERE NEW.email = email;
        IF (NEW.totalprice > saldoRestoPay) then
          raise exception 'Pastikan saldo Anda cukup untuk melakukan penarikan';
        END IF;
      END IF;
      RETURN NEW;
    END IF;
  END;
$$
LANGUAGE plpgsql; 

create trigger triggerCheckSaldoRestoPay
before insert or update on transaction 
for each row
execute procedure checkSaldoRestoPay();

-- Trigger 3 (iky)
CREATE OR REPLACE FUNCTION cekTarifPengiriman()
RETURNS trigger AS
$$
	BEGIN
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
		  IF (NEW.carfee < 2000 OR NEW.motorfee < 2000) THEN
  			RAISE EXCEPTION 'Biaya Pengiriman tidak boleh kurang dari 2000';
      END IF;
  		IF (NEW.carfee > 7000 OR NEW.motorfee > 7000) THEN
  			RAISE EXCEPTION 'Biaya Pengiriman tidak boleh lebih dari 7000';
      END IF;
  		IF (NEW.motorfee > NEW.carfee) THEN
  			RAISE EXCEPTION 'Biaya pengiriman dengan Motor harus lebih rendah dari Biaya pengiriman dengan Mobil';
  		END IF;	
  		RETURN NEW;
    END IF;
	END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER trigger_cekTarifPengiriman
BEFORE INSERT OR UPDATE ON DELIVERY_FEE_PER_KM
FOR EACH ROW 
EXECUTE PROCEDURE cekTarifPengiriman();

-- Trigger 4 (dcm)

create or replace function calculateOngkir()
returns trigger as 
$$
  declare
    car_fee int;
    motor_fee int;
    vehicle_type varchar;
    df_id varchar;
  begin  
    if (tg_op = 'INSERT') then
      select id into df_id
      from delivery_fee_per_km as d
      where new.province = d.province;
    
      select carfee into car_fee
      from delivery_fee_per_km as df
      where df.id = df_id;
  
      select motorfee into motor_fee
      from delivery_fee_per_km as df
      where df.id = df_id;
  
      select vehicletype into vehicle_type
      from courier as c
      where email = new.courierid;
  
      if (vehicle_type = 'Mobil') then
        new.deliveryfee = car_fee * 2;
      else
        new.deliveryfee = motor_fee * 2;
      end if;

      new.dfid = df_id;
      new.totalprice = new.totalfood + new.deliveryfee - new.totaldiscount;
    end if;

    if (tg_op = 'UPDATE') then
      new.totalprice = new.totalfood + new.deliveryfee - new.totaldiscount; 
    end if;
    
    return new;
  end;
$$
language plpgsql;

create trigger triggerCalculateOngkir
before insert or update on transaction
for each row
execute procedure calculateOngkir();

create or replace function calculateTotalFood() 
returns trigger as 
$$
  declare
    food_price float;
    total_discount_percent float;
    old_discount float;
    new_discount float;
  begin
    select price into food_price
    from food as f
    where f.rname = new.rname and 
    f.rbranch = new.rbranch and 
    f.foodname = new.foodname;

    select sum(discount) into total_discount_percent
    from restaurant_promo as rp, promo as p
    where rp.pid = p.id and
    rp.rname = new.rname and 
    rp.rbranch = new.rbranch and
    rp.start_promo <= now() and now() < rp.end_promo;

    if (total_discount_percent is null) then
      total_discount_percent = 0;
    end if;

    if (total_discount_percent > 100) then
      total_discount_percent = 100;
    end if;

    new_discount = 1.0 * total_discount_percent/100 * (food_price*new.amount);
    
    if (tg_op = 'INSERT') then
      update transaction 
      set totalfood = totalfood + food_price * new.amount,
      totaldiscount = totaldiscount + new_discount
      where email = new.email and 
      datetime = new.datetime;
    end if;

    if (tg_op = 'UPDATE') then 
      old_discount = 1.0 * total_discount_percent/100 * (food_price*old.amount);
      
      update transaction 
      set totalfood = totalfood + food_price * (-old.amount + new.amount),
      totaldiscount = totaldiscount + (-old_discount + new_discount)
      where email = new.email and 
      datetime = new.datetime;
    end if;

    return new;
  end;
$$
language plpgsql;

create trigger triggerCalculateTotalFood
before insert or update on transaction_food
for each row 
execute procedure calculateTotalFood();

-- Trigger 5 (divany)

create or replace function pesanan_selesai() returns trigger as
$$
  DECLARE
    biayaantar bigint;
    idkurir varchar(50);
    totalmakanan bigint;
    namaresto varchar(25);
    namacabang varchar(25);
    emailresto varchar(50);

  BEGIN
    select (deliveryfee :: bigint) into biayaantar
    from transaction
    where email = new.email AND datetime = new.datetime;

    select courierid into idkurir
    from transaction
    where email = new.email AND datetime = new.datetime;

    select (totalfood :: bigint) into totalmakanan
    from transaction
    where email = new.email AND datetime = new.datetime;

    select rname into namaresto
    from transaction_food
    where email = new.email AND datetime = new.datetime;

    select rbranch into namacabang
    from transaction_food
    where email = new.email AND datetime = new.datetime;

    select email into emailresto
    from restaurant
    where rname = namaresto AND rbranch = namacabang;


    IF(NEW.tsId = '0000000000000000000000004') then
      update transaction_actor set restopay = restopay + biayaantar where email = idkurir;
      update transaction_actor set restopay = restopay + totalmakanan where email = emailresto;
    end if;

    return new;
  end;

$$
language plpgsql;

create trigger trigger_pesanan_selesai
after insert on transaction_history
for each row execute procedure pesanan_selesai();

-- Trigger 6 UDAH BENAR

CREATE OR REPLACE FUNCTION cekPeriodePromo()
RETURNS trigger AS
$$
	DECLARE 
		sp_date timestamp;
	BEGIN
		IF(TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
			SELECT date INTO sp_date

			FROM SPECIAL_DAY_PROMO
			WHERE NEW.Pid = Id
			GROUP BY Id, sp_date;
			IF(NEW.start_promo > sp_date OR NEW.end_promo < sp_date) THEN
				RAISE EXCEPTION 'Maaf tanggal promo hari spesial harus masuk ke dalam durasi promo restaurant';
			END IF;
			RETURN NEW;
		END IF;
	END;
$$
LANGUAGE plpgsql;


create trigger triggerCekPeriodePromo
before insert or update on restaurant_promo
for each row
execute procedure cekPeriodePromo();

-- Authentication

create table session (
  id varchar(20) not null,
  email varchar(50) not null,
  opened_at timestamp not null,
  closed_at timestamp,
  primary key (id),
  foreign key (email) references user_acc (email) on delete cascade on update cascade
);

-- create table test (
--   id varchar(2) not null,
--   x int not null,
--   y int not null,
--   primary key (id)
-- );

-- create or replace function calculateTest()
-- returns trigger AS
-- $$
--   begin
--     if (tg_op = 'UPDATE') then
--       new.y = new.x;
--     end if;
--     return new;
--   end;
-- $$
-- language plpgsql;

-- create trigger triggerCaclucateTest
-- before update on test
-- for each row
-- execute procedure calculateTest();

-- insert into test values ('00', 0, 0);
-- update test set y = 10 where id = '00';