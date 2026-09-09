program rescale_to_unit
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: res(:)
  real(dp) :: min_val, max_val, range
  integer :: i

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers

  ! Find min and max
  min_val = numbers(1)
  max_val = numbers(1)
  do i = 2, numbers_len
    if (numbers(i) < min_val) min_val = numbers(i)
    if (numbers(i) > max_val) max_val = numbers(i)
  end do

  ! Calculate range
  range = max_val - min_val

  ! Allocate result array
  allocate(res(numbers_len))

  ! Rescale
  do i = 1, numbers_len
    res(i) = (numbers(i) - min_val) / range
  end do

  ! Output result
  print *, res

end program rescale_to_unit