from app import db

class RunInfo(db.Model):
    ## HiSeq + MiSeq + NextSeq
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.String(50), nullable=False)
    experiment_name = db.Column(db.String(100), nullable=False)
    run_start_date = db.Column(db.Date, nullable=False)

    #HiSeq + MiSeq
    barcode = db.Column(db.String(50))

    #HiSeq
    run_mode = db.Column(db.String(20))
    pair_end_fc = db.Column(db.Boolean)
    read_1 = db.Column(db.Integer)
    read_2 = db.Column(db.Integer)
    index_read_1 = db.Column(db.Integer)
    index_read_2 = db.Column(db.Integer)
    pe = db.Column(db.String(50))

    #NextSeq
    #chemistry =
    #flow_cell_serial =
    #is_paired_end =
    #planned_read_1_cycles =
    #planned_read_2_cycles =
    #planned_index_1_read_cycles =
    #planned_index_2_read_cycles =

    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=False)
    platform = db.relationship('Platform', backref=db.backref('runs', lazy='dynamic'))

    #def __init__(self, run_id, experiment_name):
        #self.run_id = run_id
        #self.experiment_name = experiment_name

    def __repr__(self):
	return "{} \t {} \t {}".format(self.run_id, self.experiment_name, self.run_start_date)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    application_name = db.Column(db.String(80), unique=True)

    def __init__(self, name, application_name):
        self.name = name
        self.application_name = application_name
