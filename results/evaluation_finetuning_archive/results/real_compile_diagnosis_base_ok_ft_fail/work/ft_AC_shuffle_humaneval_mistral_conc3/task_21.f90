program rescale_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: rescaled(:)
  real(dp) :: min_val, max_val

  ! Read input
  read(*, *) numbers_len
  allocate(numbers(numbers_len))
  read(*, *) numbers

  ! Calculate min and max
  min_val = minval(numbers)
  max_val = maxval(numbers)

  ! Rescale to unit range
  if (max_val > min_val) then
    rescaled = (numbers - min_val) / (max_val - min_val)
  else
    rescaled = 0.0_dp
  end if

  ! Output result
  print *, 'Rescaled values:'
  print *, rescaled

end program rescale_demo