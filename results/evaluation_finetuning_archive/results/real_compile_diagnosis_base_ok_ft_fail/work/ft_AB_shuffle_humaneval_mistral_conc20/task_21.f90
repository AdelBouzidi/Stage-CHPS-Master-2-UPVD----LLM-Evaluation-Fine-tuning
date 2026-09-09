program rescale_to_unit_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: res(:)
  real(dp) :: min_val, max_val

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers

  ! Rescale to unit interval
  min_val = minval(numbers)
  max_val = maxval(numbers)
  if (max_val == min_val) then
    res = 0.0_dp
  else
    res = (numbers - min_val) / (max_val - min_val)
  end if

  ! Output result
  print *, res

end program rescale_to_unit_demo