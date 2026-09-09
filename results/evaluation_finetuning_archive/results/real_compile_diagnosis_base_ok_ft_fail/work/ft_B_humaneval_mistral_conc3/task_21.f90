program rescale_to_unit
  implicit none
  integer, parameter :: n = 5
  real :: numbers(n), rescaled(n)
  integer :: i
  real :: min_val, max_val

  ! Read input
  read(*,*) n
  read(*,*) (numbers(i), i = 1, n)

  ! Find min and max
  min_val = numbers(1)
  max_val = numbers(1)
  do i = 2, n
    if (numbers(i) < min_val) min_val = numbers(i)
    if (numbers(i) > max_val) max_val = numbers(i)
  end do

  ! Apply rescaling
  do i = 1, n
    rescaled(i) = (numbers(i) - min_val) / (max_val - min_val)
  end do

  ! Output result
  do i = 1, n
    write(*,*) rescaled(i)
  end do

end program rescale_to_unit