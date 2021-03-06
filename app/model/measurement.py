from app import db


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batchId = db.Column(db.Integer, db.ForeignKey('batch.id'))
    sampleId = db.Column(db.Integer, db.ForeignKey('sample.id'))
    t_to = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    t_amp = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    t = db.Column(db.Numeric(precision=6, scale=3), nullable=True)
    s_to = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    s_amp = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    s = db.Column(db.Numeric(precision=6, scale=3), nullable=True)
    ts = db.Column(db.Numeric(precision=12, scale=6), nullable=True)
    errorCode = db.Column(db.String(50))
    errorLowT_to = db.Column(db.Boolean(), nullable=True)
    errorHighCv = db.Column(db.Boolean(), nullable=True)
    errorInvalidSampleCount = db.Column(db.Boolean(), nullable=True)
    coefficientOfVariation = db.Column(
        db.Numeric(precision=12, scale=6), nullable=True)

    batch = db.relationship("Batch", backref=db.backref(
        'measurements',
        order_by=id,
        cascade="all, delete-orphan"))
    sample = db.relationship("Sample", backref=db.backref(
        'measurements',
        order_by=id,
        cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.batchId = kwargs.get('batchId')
        self.sampleId = kwargs.get('sampleId')
        self.t_to = kwargs.get('t_to')
        self.t_amp = kwargs.get('t_amp')
        self.t = kwargs.get('t')
        self.s_to = kwargs.get('s_to')
        self.s_amp = kwargs.get('s_amp')
        self.s = kwargs.get('s')
        primerBatch = kwargs.get('primerBatch')

        if (primerBatch in [3, 4, 6]):
            t_to_minimum = 11.7
        elif primerBatch == 5:
            t_to_minimum = 12.2
        elif primerBatch == 7:
            t_to_minimum = 11.3
        else:
            t_to_minimum = 12.4

        if self.t is not None and self.s is not None:
            self.ts = round(self.t / self.s, 6)

        self.errorLowT_to = (self.t_to < t_to_minimum)
        self.errorCode = kwargs.get('errorCode')

    def GetValidationErrors(self):
        result = []
        errorCodeReported = False

        if self.t_to is None:
            result.append(self._missingErrorDescription('t_to'))
        elif self.errorLowT_to and str(self.errorCode) != '2':
            result.append(
                "Measurement has T_TO value of {0:.2f}, "
                "but does not have error code of '2'".format(self.t_to))
            errorCodeReported = True
        elif (not self.errorLowT_to) and str(self.errorCode) == '2':
            result.append(
                "Measurement has T_TO value of {0:.2f}, "
                "but has been given an error code of '2'".format(self.t_to))
            errorCodeReported = True
        elif self.errorLowT_to and str(self.errorCode) == '2':
            result.append(
                "Validated error code '2': T_TO = {0:.2f}.".format(self.t_to))
            errorCodeReported = True

        if str(self.errorCode) != '' and not errorCodeReported:
            result.append("Error code of {0}".format(self.errorCode))

        if self.t_amp is None:
            result.append(self._missingErrorDescription('t_amp'))

        if self.t is None:
            result.append(self._missingErrorDescription('t'))

        if self.s_to is None:
            result.append(self._missingErrorDescription('s_to'))

        if self.s_amp is None:
            result.append(self._missingErrorDescription('s_amp'))

        if self.s is None:
            result.append(self._missingErrorDescription('s'))

        if self.errorInvalidSampleCount:
            result.append(
                "Sample does not have the correct amount "
                "of ts values to calculate a CV.")

        if self.coefficientOfVariation is not None:
            if self.errorHighCv and str(self.errorCode) != '1':
                result.append(
                    "Samples have a coefficient of variation of {0:.2f}, "
                    "but do not have an error code of '1'"
                    .format(self.coefficientOfVariation))
            elif (not self.errorHighCv) and str(self.errorCode) == '1':
                result.append(
                    "Samples have a coefficient of variation of {0:.2f}, "
                    "but have been given an error code of '1'"
                    .format(self.coefficientOfVariation))
            elif self.coefficientOfVariation and str(self.errorCode) == '1':
                result.append(
                    "Validated error code '1': "
                    "Sample coefficient of variation = {0:.2f}"
                    .format(self.coefficientOfVariation))
        elif str(self.errorCode) == '1':
            result.append(
                "Samples coefficient of variation cannot be calculated, "
                "but have been given an error code of '1'")

        return result

    def is_error_free(self):
        return len(self.GetValidationErrors()) == 0

    def _missingErrorDescription(self, fieldname):
        return "'%s' is missing or not valid" % fieldname
