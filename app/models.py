from app import db

class RunInfo(db.Model):
    ## Required
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.String(50), nullable=False)
    experiment_name = db.Column(db.String(100), nullable=False)
    run_start_date = db.Column(db.Date, nullable=False)
    barcode = db.Column(db.String(50), nullable=False)

    run_mode = db.Column(db.String(50))
    paired_end = db.Column(db.Boolean)
    read_1 = db.Column(db.Integer)
    read_2 = db.Column(db.Integer)
    index_read_1 = db.Column(db.Integer)
    index_read_2 = db.Column(db.Integer)
    pe = db.Column(db.String(50))

    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=False)
    platform = db.relationship('Platform', backref=db.backref('runs', lazy='dynamic'))

    def __repr__(self):
        return "{} \t {} \t {}".format(self.run_id, self.experiment_name, self.run_start_date)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    application_name = db.Column(db.String(80), unique=True)

    def __init__(self, name, application_name):
        self.name = name
        self.application_name = application_name
