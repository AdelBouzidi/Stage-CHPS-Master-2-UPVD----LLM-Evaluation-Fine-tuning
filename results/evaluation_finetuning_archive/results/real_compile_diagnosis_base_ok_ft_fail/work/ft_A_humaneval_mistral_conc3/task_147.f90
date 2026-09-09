program main
  implicit none
  integer :: n
  integer, allocatable :: a(:)
  integer :: count

  ! Read input n
  read(*,*) n

  ! Create array a
  allocate(a(n))
  a = [(i*i - i + 1, i = 1, n)]

  ! Count triples with sum divisible by 3
  count = 0
  do k = 3, n
    do j = 2, k-1
      do i = 1, j-1
        if (mod(a(i) + a(j) + a(k), 3) == 0) then
          count = count + 1
        end if
      end do
    end do
  end do

  ! Output result
  print *, count

  deallocate(a)
end program main