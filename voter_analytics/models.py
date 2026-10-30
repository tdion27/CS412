from django.db import models

# Create your models here.
class Voter(models.Model):
    '''store and represent the data from one registered voter'''
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.TextField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Create a string representation of a voter.'''
        return f'{self.first_name} {self.last_name}'


def load_data():
    '''the function to load data records from the file into the django model'''
    Voter.objects.all().delete()
    filename = '/Users/thomasdion/Downloads/newton_voters.csv' 
    f = open(filename)
    f.readline()

    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Voter object with this record from CSV
            # Using .strip() ensures we remove invisible newline characters or extra spaces
            voter = Voter(last_name=fields[1],
                          first_name=fields[2],
                          street_number=fields[3],
                          street_name=fields[4],
                          apartment_number=fields[5],
                          zip_code=fields[6],
                          date_of_birth=fields[7],
                          date_of_registration=fields[8],
                          party_affiliation=fields[9],
                          precinct_number=fields[10],
                          v20state=fields[11] == 'TRUE',
                          v21town=fields[12] == 'TRUE',
                          v21primary=fields[13] == 'TRUE',
                          v22general=fields[14] == 'TRUE',
                          v23town=fields[15] == 'TRUE',
                          voter_score=fields[16],
                         )
            voter.save()
            print(f'Created voter: {voter}')
        except:
            print(f"Skipped: {fields}")
    print(f'Done. Created {len(Voter.objects.all())} Voters.')