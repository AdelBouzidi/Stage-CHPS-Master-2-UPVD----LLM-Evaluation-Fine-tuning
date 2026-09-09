program rescale_to_unit
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: res(:)
  
  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers
  
  ! Call the function
  call rescale_to_unit(numbers_len, numbers, res)
  
  ! Output results
  print *, numbers_len
  print *, res
contains
  subroutine rescale_to_unit(numbers_len, numbers, res)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(numbers_len)
    real(dp), intent(out) :: res(numbers_len)
    real(dp) :: min_val, max_val
    
    min_val = minval(numbers)
    max_val = maxval(numbers)
    
    if (max_val == min_val) then
      res = 0.0_dp
    else
      res = (numbers - min_val) / (max_val - min_val)
    end if
  end subroutine rescale_to_unit
end program rescale_to_unit