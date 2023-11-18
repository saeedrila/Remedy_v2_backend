from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)
from appointments.views import (
    FetchPatientAppointData,
    FetchDoctorAppointData,
    FetchLabAppointData,
    FetchAllAppointData,
    AppointmentPrescription,
    AppointmentReport,
    FetchExecutiveDashboardData,
    FetchDoctorDashboardData,
    FetchLabDashboardData,
)
from authentication.views import (
    AccountSignup,
    AccountLogin,
    LogoutView,
    ChangePassword,
    ActivateUser,
    TestAPIView,
)
from chat.views import (
    ChatAPI,
    MyInbox,
    GetMessages,
    SendMessages,
    InitiateChatOnAppointment,
)
from doctors_and_labs.views import (
    DoctorAvailabilityRegistration,
    LabAvailabilityRegistration,
    DoctorAccountDetails,
    LabAccountDetails,
    GetListOfSpecialization,
    GetListOfSpecializationForHome,
    GetListOfTestsForHome,
    DoctorSpecificSpecialization,
    DoctorsListAtSpecialization,
    GetListOfTests,
    LabSpecificTest,
)
from executives.views import AccountApproval
from patients.views import (
    GetPatientProfileDetails,
    PatchProfileDetails,
    FetchAvailableTimingDoctor,
    FetchAvailableTimingLab,
)
from payments.views import (
    CheckoutPayment,
    RazorpayOrder,
    RazorpayOrderComplete,
    GetExecutivePaymentList,
    GetDoctorPaymentList,
    GetLabPaymentList,
    GetPatientPaymentList,
)
from reports.views import ProfileImage



urlpatterns = [
    path('admin/', admin.site.urls),

#JWT Refresh and access tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # for obtaining access tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # for refreshing tokens
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

#Authentication
    # URL for backend working checking
    path('', TestAPIView.as_view(), name='all-account-list'),

    # Signup, Login, and Logout API endpoints
    # Add account, Patient, Doctor, Lab, Executive accounts
    path('api/account-signup', AccountSignup.as_view(), name='account-signup'),
    path('api/account-login', AccountLogin.as_view(), name='patient-login'),
    path('api/logout', LogoutView.as_view(), name='logout-view'),
    path('api/change-password', ChangePassword.as_view(), name='change-password'),

    # Activate user by Executive
    path('api/activate-user', ActivateUser.as_view(), name='activate-user'),

#Executive
    path('api/account-approval', AccountApproval.as_view(), name='account_approval'),


#Appointments
    # Get appointments
    path('api/fetch-patient-appointments', FetchPatientAppointData.as_view(), name='fetch_patient_appointments'),
    path('api/fetch-doctor-appointments', FetchDoctorAppointData.as_view(), name='fetch_doctor_appointments'),
    path('api/fetch-lab-appointments', FetchLabAppointData.as_view(), name='fetch_lab_appointments'),
    path('api/fetch-all-appointments', FetchAllAppointData.as_view(), name='fetch_all_appointments'),

    # Get and patch prescription
    path('api/fetch-prescription', AppointmentPrescription.as_view(), name='fetch-prescription'),
    path('api/patch-prescription', AppointmentPrescription.as_view(), name='fetch-prescription'),
    path('api/patch-report', AppointmentReport.as_view(), name='patch-report'),
    path('api/fetch-patient-prescription', AppointmentPrescription.as_view(), name='fetch-patient-prescription'),

    # Get data for dashboard
    path('api/fetch-executive-dashboard-data', FetchExecutiveDashboardData.as_view(), name='fetch-executive-dashboard-data'),
    path('api/fetch-doctor-dashboard-data', FetchDoctorDashboardData.as_view(), name='fetch-doctor-dashboard-data'),
    path('api/fetch-lab-dashboard-data', FetchLabDashboardData.as_view(), name='fetch-lab-dashboard-data'),
    

#Chat
    path('api/chat', ChatAPI.as_view(), name='chat-api-view'),
    path('api/my-messages/<user_id>', MyInbox.as_view()),
    path("api/get-messages/<sender_id>/<reciever_id>", GetMessages.as_view()),
    path("api/send-messages", SendMessages.as_view()),
    path("api/initiate-chat-on-appointment", InitiateChatOnAppointment.as_view()),
    

#Doctors and Labs
    # Get doctor availability
    path('api/doctor-availability-get-url', DoctorAvailabilityRegistration.as_view(), name='doctor-availability-get-url'),
    # Get and Patch doctor account details
    path('api/get-doctor-account-details', DoctorAccountDetails.as_view(), name='doctor_account_details'),
    # Get and Post doctor specialization details
    path('api/doctor-specialization-generic-url', GetListOfSpecialization.as_view(), name='doctor_specialization_url'),
    path('api/doctor-specialization-for-home', GetListOfSpecializationForHome.as_view(), name='doctor-specialization-for-home'),
    # Specific url for getting a doctor's specialization details
    path('api/doctor-specialization-specific', DoctorSpecificSpecialization.as_view(), name='doctor_specialization_specific'),
    # Fetch available doctors on a particular specialization
    path('api/doctors-at-specific-specialization/', DoctorsListAtSpecialization.as_view(), name='doctors-at-specialization'),

    # Get Lab availability
    path('api/lab-availability-get-url', LabAvailabilityRegistration.as_view(), name='lab-availability-get-url'),
    # Get and Patch lab account details
    path('api/get-lab-account-details', LabAccountDetails.as_view(), name='lab_account_details'),
    # Get and Post doctor specialization details
    path('api/get-all-lab-tests', GetListOfTests.as_view(), name='get-all-lab-tests'),
    path('api/lab-tests-for-home', GetListOfTestsForHome.as_view(), name='lab-tests-for-home'),
    # Specific url for getting a lab's specialization details
    path('api/get-lab-specific-test', LabSpecificTest.as_view(), name='get-lab-specific-test'),

#Patients
    # Get patient profile details from 'Account' model
    path('api/get-patient-profile-details', GetPatientProfileDetails.as_view(), name='get-patient-profile-detials'),
    path('api/patch-profile-details', PatchProfileDetails.as_view(), name='patch-profile-detials'),

    # Get available timing of doctors
    path('api/fetch-per-day-availability-of-specialized-doctor/', FetchAvailableTimingDoctor.as_view(), name='fetch-per-day-availability-of-sepecialized-doctor'),
    path('api/fetch-per-day-availability-of-lab/', FetchAvailableTimingLab.as_view(), name='fetch-per-day-availability-of-lab'),


#Payments
    # Razorpay payment testing
    path('api/checkout_payment', CheckoutPayment.as_view(), name='checkout-payment'),
    path('api/razorpay/order/create', RazorpayOrder.as_view(), name='razorpay-order-create'),
    path('api/razorpay/order/complete', RazorpayOrderComplete.as_view(), name='razorpay-order-complete'),

    #Payment list fetching
    path('api/fetch-executive-payments', GetExecutivePaymentList.as_view(), name='fetch-executive-payments'),
    path('api/fetch-doctor-payments', GetDoctorPaymentList.as_view(), name='fetch-doctor-payments'),
    path('api/fetch-lab-payments', GetLabPaymentList.as_view(), name='fetch-lab-payments'),
    path('api/fetch-patient-payments', GetPatientPaymentList.as_view(), name='fetch-patient-payments'),

#Reports
    # File upload
    path('api/upload-profile-image', ProfileImage.as_view(), name='upload-profile-image'),

]
