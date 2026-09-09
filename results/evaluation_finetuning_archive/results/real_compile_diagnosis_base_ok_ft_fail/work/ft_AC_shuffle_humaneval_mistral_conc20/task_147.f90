program get_max_triples
  implicit none
  integer :: n
  integer, allocatable :: a(:)
  integer :: i, j, k, count

  ! Read input
  read(*,*) n

  ! Allocate array
  allocate(a(n))

  ! Fill array with values
  do i = 1, n
    a(i) = i*i - i + 1
  end do

  ! Count triples
  count = 0
  do i = 1, n-2
    do j = i+1, n-1
      do k = j+1, n
        if (mod(a(i) + a(j) + a(k), 3) == 0) then
          count = count + 1
        end if
      end do
    end do
  end do

  ! Output result
  print *, count

  ! Clean up
  deallocate(a)

end program get_max_triples