program rescale_to_unit
            implicit none
            integer :: numbers_len
            real :: numbers(10)
            real :: res
            real, allocatable :: rescale(:)
            real :: numbers_in(10)
            real :: numbers_out(10)
            integer :: i
            !
            numbers_len = 5
            numbers = (/ 1.0, 2.0, 3.0, 4.0, 5.0 /)
            !
            rescale = rescale_to_unit(numbers_len, numbers)
            !
            print *, 'rescale_to_unit'
            print *, numbers_len
            print *, rescale
            !
            end program rescale_to_unit