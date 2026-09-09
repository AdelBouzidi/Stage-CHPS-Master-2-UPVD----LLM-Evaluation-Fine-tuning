program rescale_to_unit
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: n
  real(dp), allocatable :: numbers(:)
  real(dp), allocatable :: result(:)
  integer :: i
  
  ! Read input
  read(*,*) n
  allocate(numbers(n))
  read(*,*) numbers
  
  ! Compute min and max
  real(dp) :: min_val, max_val
  min_val = numbers(1)
  max_val = numbers(1)
  do i = 2, n
    if (numbers(i) < min_val) min_val = numbers(i)
    if (numbers(i) > max_val) max_val = numbers(i)
  end do
  
  ! Apply linear transform
  allocate(result(n))
  if (max_val == min_val) then
    result = 0.0_dp
  else
    result = (numbers - min_val) / (max_val - min_val)
  end if
  
  ! Output result
  write(*,*) result
end program rescale_to_unit